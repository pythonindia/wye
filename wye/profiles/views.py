# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template import Context, loader
from django.views.generic import UpdateView
from django.views.generic.list import ListView
from django.contrib.auth import logout
from wye.base.constants import WorkshopStatus
from wye.base.emailer_html import send_email_to_id, send_email_to_list
from wye.organisations.models import Organisation
from wye.profiles.models import Profile
from wye.workshops.models import Workshop

from .forms import ContactUsForm, UserProfileForm, PartnerForm


def profile_view(request, slug):
    try:
        p = Profile.objects.get(user__username=slug)
        workshops = Workshop.objects.filter(
            presenter=p.user).order_by('-expected_date')
        return render(
            request, 'profile/index.html',
            {'object': p, 'workshops': workshops})
    except Profile.DoesNotExist:
        return render(request, 'error.html', {
            "message": "Profile does not exist"})


class UserDashboard(ListView):
    model = Profile
    template_name = 'profile/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        user_profile = get_object_or_404(
            Profile, user__id=self.request.user.id)
        if not user_profile.get_user_type:
            return redirect('profiles:profile-edit',
                            slug=request.user.username)
        return super(UserDashboard, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDashboard, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        workshop_all = Workshop.objects.all()
        accept_workshops = workshop_all.filter(
            status=WorkshopStatus.ACCEPTED)
        requested_workshops = workshop_all.filter(
            status=WorkshopStatus.REQUESTED)
        organisation_all = Organisation.objects.all()
        for each_type in profile.get_user_type:
            if each_type == 'tutor':
                context['is_tutor'] = True
                context['workshop_requested_tutor'] = accept_workshops.filter(
                    presenter=self.request.user)
                context['workshop_completed_tutor'] = \
                    requested_workshops.filter(
                    presenter=self.request.user)
            if each_type == 'lead':
                context['is_regional_lead'] = True
                context['workshops_accepted_under_rl'] = accept_workshops
                context['workshops_pending_under_rl'] = requested_workshops
                context['interested_tutors'] = Profile.objects.filter(
                    usertype__slug='tutor',
                    interested_locations__name__in=profile.get_interested_locations)\
                    .exclude(user=self.request.user).count()
                context['interested_locations'] = organisation_all.filter(
                    location__name__in=profile.get_interested_locations)\
                    .count()

            if each_type == 'poc':
                context['is_college_poc'] = True
                context['users_organisation'] = organisation_all.filter(
                    user=self.request.user)
                context['workshop_requested_under_poc'] = workshop_all.filter(
                    requester__id__in=organisation_all.values_list(
                        'id', flat=True))
                context['workshops_accepted_under_poc'] = workshop_all.filter(
                    status=WorkshopStatus.ACCEPTED,
                    requester__id__in=organisation_all.values_list(
                        'id', flat=True))

            if each_type == 'admin':
                context['is_admin'] = True
                context['workshops_by_status'] = workshop_all.order_by(
                    'status')
                context['workshops_by_region'] = workshop_all.order_by(
                    'location')

        return context


class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'profile/update.html'
    form_class = UserProfileForm
    slug_field = 'user__username'

    def form_valid(self, form):
        return super(ProfileEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profiles:profile-page', kwargs={
            'slug': self.object.slug})

    def dispatch(self, *args, **kwargs):
        if self.request.user.pk == self.get_object().pk:
            return super(ProfileEditView, self).dispatch(*args, **kwargs)
        else:
            raise PermissionDenied


def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            email_context = Context({
                'contact_name': form.cleaned_data['name'],
                'contact_email': form.cleaned_data['email'],
                'comments': form.cleaned_data['comments'],
                'conatct_number': form.cleaned_data['contact_number'],
                'feedback_type': form.cleaned_data['feedback_type']
            })

            subject = "PythonExpress Feedback by %s" % (
                form.cleaned_data['name'])
            text_body = loader.get_template(
                'email_messages/contactus/message.txt').render(email_context)
            email_body = loader.get_template(
                'email_messages/contactus/message.html').render(email_context)
            user_subject = '[PythonExpress] Feedback Received'
            user_text_body = loader.get_template(
                'email_messages/contactus/message_user.txt').render(
                email_context)
            user_email_body = loader.get_template(
                'email_messages/contactus/message_user.html').render(
                email_context)

            try:
                regional_lead = Profile.objects.filter(
                    usertype__slug__in=['lead', 'admin']).values_list(
                    'user__email', flat=True)
                send_email_to_list(
                    subject,
                    users_list=regional_lead,
                    body=email_body,
                    text_body=text_body)

                send_email_to_id(
                    user_subject,
                    body=user_email_body,
                    email_id=form.cleaned_data['email'],
                    text_body=user_text_body)
            except Exception as e:
                print(e)
            return HttpResponseRedirect('/thankyou')
    else:
        form = ContactUsForm()
    return render(request, 'contact.html', {'form': form})


def partner_view(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            email_context = Context({
                'org_name': form.cleaned_data['org_name'],
                'org_url': form.cleaned_data['org_url'],
                'partner_type': form.cleaned_data['partner_type'],
                'description': form.cleaned_data['description'],
                'python_use': form.cleaned_data['python_use'],
                'comments': form.cleaned_data['comments'],
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'contact_name': form.cleaned_data['name'],
                'contact_email': form.cleaned_data['email'],
                'conatct_number': form.cleaned_data['contact_number'],

            })

            subject = "[PythonExpress] Partnership request by %s" % (
                form.cleaned_data['org_name'])
            text_body = loader.get_template(
                'email_messages/partner/partner_message.txt').render(
                email_context)
            email_body = loader.get_template(
                'email_messages/partner/partner_message.html').render
            (email_context)
            user_subject = '[PythonExpress] Partnership request Received'
            user_text_body = loader.get_template(
                'email_messages/partner/message_user.txt').render(
                email_context)
            user_email_body = loader.get_template(
                'email_messages/partner/message_user.html').render(
                email_context)

            try:
                send_email_to_list(
                    subject,
                    users_list=['contact@pythonexpress.in'],
                    body=email_body,
                    text_body=text_body)

                send_email_to_id(
                    user_subject,
                    body=user_email_body,
                    email_id=form.cleaned_data['email'],
                    text_body=user_text_body)
            except Exception as e:
                print(e)
            return HttpResponseRedirect('/thankyou')
    else:
        form = PartnerForm()
    return render(request, 'partner.html', {'form': form})


def account_deactivate(request, slug):
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    return HttpResponseRedirect('/')
