from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import UpdateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.template import Context, loader

from wye.base.emailer_html import send_email_to_list, send_email_to_id
from wye.base.constants import WorkshopStatus
from wye.organisations.models import Organisation
from wye.workshops.models import Workshop

from . import models
from .forms import UserProfileForm, ContactUsForm


class ProfileView(DetailView):
    model = models.Profile
    template_name = 'profile/index.html'
    slug_field = 'user__username'

    def get_context_data(self, *args, **kwargs):
        slug = self.kwargs['slug']
        self.object = self.model.objects.get(user__username=slug)
        context = super(
            ProfileView, self).get_context_data(*args, **kwargs)
        return context


class UserDashboard(ListView):
    model = models.Profile
    template_name = 'profile/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        user_profile = models.Profile.objects.get(
            user__id=self.request.user.id)
        if not user_profile.get_user_type:
            return redirect('profiles:profile-edit', slug=request.user.username)
        return super(UserDashboard, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDashboard, self).get_context_data(**kwargs)
        user_profile = models.Profile.objects.get(
            user__id=self.request.user.id)
        workshop_all_list = Workshop.objects.all()
        my_organisation_list = Organisation.objects.filter(
            user=self.request.user)
        print(user_profile.get_user_type)
        for each_type in user_profile.get_user_type:
            if each_type == 'tutor':
                context['is_tutor'] = True
                context['workshop_requested_tutor'] = workshop_all_list.filter(
                    presenter=self.request.user, status=WorkshopStatus.REQUESTED)
                context['workshop_completed_tutor'] = workshop_all_list.filter(
                    presenter=self.request.user, status=WorkshopStatus.COMPLETED)
            if each_type == 'lead':
                context['is_regional_lead'] = True
                context['workshops_accepted_under_rl'] = workshop_all_list.filter(
                    status=WorkshopStatus.ACCEPTED)
                context['workshops_pending_under_rl'] = workshop_all_list.filter(
                    status=WorkshopStatus.REQUESTED)
                context['interested_tutors'] = models.Profile.objects.filter(
                    usertype__slug='tutor',
                    interested_locations__name__in=user_profile.get_interested_locations).exclude(
                    user__id=self.request.user.id).count()
                context['interested_locations'] = Organisation.objects.filter(
                    location__name__in=user_profile.get_interested_locations).count()
            if each_type == 'poc':
                context['is_college_poc'] = True
                context['users_organisation'] = my_organisation_list
                context['workshop_requested_under_poc'] = workshop_all_list.filter(
                    requester__id__in=my_organisation_list.values_list('id', flat=True))
                context['workshops_accepted_under_poc'] = workshop_all_list.filter(
                    status=WorkshopStatus.ACCEPTED,
                    requester__id__in=my_organisation_list.values_list('id', flat=True))
            if each_type == 'admin':
                context['is_admin'] = True
                context['workshops_by_status'] = workshop_all_list.order_by(
                    'status')
                context['workshops_by_region'] = workshop_all_list.order_by(
                    'location')
        return context


class ProfileEditView(UpdateView):
    model = models.Profile
    template_name = 'profile/update.html'
    form_class = UserProfileForm
    slug_field = 'user__username'

    def form_valid(self, form):
        return super(ProfileEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profiles:profile-page', kwargs={'slug': self.object.slug})

    def dispatch(self, *args, **kwargs):
        if self.request.user.pk == self.get_object().pk:
            return super(ProfileEditView, self).dispatch(*args, **kwargs)
        else:
            raise PermissionDenied


class ContactFormView(FormView):
    form_class = ContactUsForm
    template_name = 'contact.html'
    success_url = '/thankyou'

    def form_valid(self, form):

        email_context = Context({
            'contact_name': form.cleaned_data['name'],
            'contact_email': form.cleaned_data['email'],
            'comments': form.cleaned_data['comments'],
            'conatct_number': form.cleaned_data['contact_number'],
            'feedback_type': form.cleaned_data['feedback_type']
        })

        subject = "PythonExpress Feedback by %s" % (form.cleaned_data['name'])
        text_body = loader.get_template(
            'email_messages/contactus/message.txt').render(email_context)
        email_body = loader.get_template(
            'email_messages/contactus/message.html').render(email_context)
        user_subject = '[PythonExpress] Feedback Received'
        user_text_body = loader.get_template(
            'email_messages/contactus/message_user.txt').render(email_context)
        user_email_body = loader.get_template(
            'email_messages/contactus/message_user.html').render(email_context)

        try:
            regional_lead = models.Profile.objects.filter(
                usertype__slug__in=['lead', 'admin']).values_list('user__email', flat=True)
            send_email_to_list(
                subject,
                users_list=regional_lead,
                body=email_body,
                text_body=text_body)
        except Exception as e:
            print(e)
        try:
            send_email_to_id(
                user_subject,
                body=user_email_body,
                email_id=form.cleaned_data['email'],
                text_body=user_text_body)
        except Exception as e:
            print(e)

        return super(ContactFormView, self).form_valid(form)
