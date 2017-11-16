# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import Context, loader
from django.views.generic import UpdateView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from wye.base.constants import WorkshopStatus
from wye.base.emailer_html import send_email_to_id, send_email_to_list
from wye.organisations.models import Organisation
from wye.profiles.models import Profile
from wye.workshops.models import Workshop

from .forms import ContactUsForm, UserProfileForm, PartnerForm


@login_required
def account_redirect(request):
    print(request.user.username)
    return redirect('/profile/{}/'.format(request.user.username))


def profile_view(request, slug):
    try:
        p = Profile.objects.get(user__username=slug)
        workshops = Workshop.objects.filter(is_active=True).filter(
            presenter=p.user).filter(status__in=[
                WorkshopStatus.ACCEPTED,
                WorkshopStatus.REQUESTED,
                WorkshopStatus.FEEDBACK_PENDING,
                WorkshopStatus.COMPLETED]).order_by('-expected_date')
        return render(
            request, 'profile/index.html',
            {'object': p, 'workshops': workshops})
    except Profile.DoesNotExist:
        return render(request, 'error.html', {
            "message": "Profile does not exist"})


# def user_dashboad(request):
#     profile, created = Profile.objects.get_or_create(
#         user__id=request.user.id)
#     if not profile.is_profile_filled:
#         return redirect('profiles:profile-edit', slug=request.user.username)
#     workshop_all = Workshop.objects.filter(
#         is_active=True).order_by('-expected_date')

#     accept_workshops = workshop_all.filter(
#         status=WorkshopStatus.ACCEPTED).filter(
#             presenter__id__in=[request.user.id])
#     requested_workshops = workshop_all.filter(
#         status=WorkshopStatus.REQUESTED).filter(
#             presenter__id__in=[request.user.id])
#     requested_workshops = workshop_all.filter(
#         status=WorkshopStatus.REQUESTED).filter(
#             presenter__id__in=[request.user.id])

#     organisation_all = Organisation.objects.all()
#     context = {}
#     for each_type in profile.get_user_type:
#         if each_type == 'poc':
#             context['is_college_poc'] = True
#             context['users_organisation'] = organisation_all.filter(
#                 user=request.user)
#             context['workshop_requested_under_poc'] = workshop_all.filter(
#                 requester__id__in=organisation_all.values_list(
#                     'id', flat=True))
#             context['workshops_accepted_under_poc'] = workshop_all.filter(
#                 status=WorkshopStatus.ACCEPTED,
#                 requester__id__in=organisation_all.values_list(
#                     'id', flat=True))
#         else:
#             context['is_tutor'] = True
#             context['workshop_requested_tutor'] = accept_workshops.filter(
#                 presenter=request.user)
#             context['workshop_completed_tutor'] = \
#                 requested_workshops.filter(
#                 presenter=request.user)


class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'profile/update.html'
    form_class = UserProfileForm
    slug_field = 'user__username'

    def form_valid(self, form):
        return super(ProfileEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profiles:profile-page', kwargs={
            'slug': self.object.user.username})

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
            site_admins = [
                email for name, email in settings.MANAGERS]  # @UnusedVariable
            try:
                regional_lead = list(Profile.objects.filter(
                    usertype__slug__in=['admin']).values_list(
                    'user__email', flat=True))
                regional_lead.extend(site_admins)
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
        if request.user.is_authenticated():
            form = ContactUsForm(initial={'name': request.user.first_name +
                                          " " + request.user.last_name,
                                          'email': request.user.email
                                          })
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
                'email_messages/partner/partner_message.html').render(
                email_context)
            user_subject = '[PythonExpress] Partnership request Received'
            user_text_body = loader.get_template(
                'email_messages/partner/message_user.txt').render(
                email_context)
            user_email_body = loader.get_template(
                'email_messages/partner/message_user.html').render(
                email_context)

            try:
                send_email_to_id(
                    subject,
                    email_id='contact@pythonexpress.in',
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
