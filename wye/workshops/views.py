from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.template import loader
from django.views import generic

from braces import views
from wye.base.emailer_html import send_email_to_list
from wye.organisations.models import Organisation
from wye.profiles.models import Profile
from wye.regions.models import RegionalLead
from wye.base.constants import WorkshopStatus

from wye.social.sites.twitter import send_tweet
from wye.base.views import verify_user_profile
from .forms import WorkshopForm, WorkshopEditForm, WorkshopFeedbackForm
from .mixins import (
    WorkshopEmailMixin,
    WorkshopAccessMixin
    )
from .models import Workshop


@login_required
@verify_user_profile
def workshop_list(request):
    template_name = 'workshops/workshop_list.html'
    user_profile, created = Profile.objects.get_or_create(
        user__id=request.user.id)
    if not user_profile.is_profile_filled:
        return redirect('profiles:profile-edit', slug=request.user.username)
    context_dict = {}
    workshop_list = Workshop.objects.all().order_by('-expected_date')
    workshop_list = workshop_list.filter(
        requester__location__id__in=[ x.id for x in
                request.user.profile.interested_locations.all()])
    # if Profile.is_organiser(request.user):
    #     workshop_list = workshop_list.filter(
    #         requester__user=request.user)
    # elif Profile.is_presenter(request.user):
    #     workshop_list = workshop_list.filter(
    #         Q(presenter=request.user) | Q
    #         (requester__location__id__in=[
    #             x.id for x in
    #             request.user.profile.interested_locations.all()]))
    # elif Profile.is_regional_lead(request.user):
    #     regions = RegionalLead.objects.filter(leads=request.user)
    #     workshop_list = workshop_list.filter(
    #         location__id__in=[x.location.id for x in regions])
    print(workshop_list)
    context_dict['workshop_list'] = workshop_list
    context_dict['user'] = request.user
    # need to improve the part
    context_dict['is_not_tutor'] = False
    # as user can be tutor and regional lead hence we need to verify like
    # this
    if (Profile.is_regional_lead(request.user) or
            Profile.is_organiser(request.user) or
            Profile.is_admin(request.user)):
        context_dict['is_not_tutor'] = True

    return render(request, template_name, context_dict)


def workshop_details(request, pk):
    template_name = 'workshops/workshop_detail.html'
    workshop_obj = get_object_or_404(Workshop, id=pk)
    context_dict = {'workshop': workshop_obj}
    return render(request, template_name, context_dict)


@login_required
@verify_user_profile
def workshop_create(request):
    template_name = 'workshops/workshop_create.html'
    context_dict = {}
    if not Organisation.list_user_organisations(request.user).exists():
        msg = """
                To request workshop you need to create organisaiton.\n\n
                Please use organisation tab above to create your organisation
            """
        return render(request, 'error.html', {'message': msg})
    if request.method == 'GET':
        form = WorkshopForm(user=request.user)
        context_dict['form'] = form
        return render(request, template_name, context_dict)
    form = WorkshopForm(user=request.user, data=request.POST)
    if not form.is_valid():
        context_dict['form'] = form
        context_dict['errors'] = form.errors
        return render(request, template_name, context_dict)
    workshop = form.save()
    context = {
        'workshop': workshop,
        'date': workshop.expected_date,
        'workshop_url': 'https://pythonexpress.in/workshop/{}/'.format(workshop.id)
    }
    # Collage POC and admin email
    poc_admin_user = Profile.get_user_with_type(
        user_type=['Collage POC', 'admin']
        ).values_list('email', flat=True)

    org_user_emails = workshop.requester.user.filter(
        is_active=True).values_list('email', flat=True)
    # all presenter if any
    all_presenter_email = workshop.presenter.values_list(
        'email', flat=True)
    # List of tutor who have shown interest in that location
    region_interested_member = Profile.objects.filter(
        interested_locations=workshop.requester.location,
        usertype__slug='tutor'
        ).values_list('user__email', flat=True)
    all_email = []
    all_email.extend(org_user_emails)
    all_email.extend(all_presenter_email)
    all_email.extend(poc_admin_user)
    all_email.extend(region_interested_member)
    all_email = set(all_email)
    send_tweet(context)

    subject = '[PythonExpress] Workshop request status.'
    email_body = loader.get_template(
        'email_messages/workshop/create_workshop/message.html').render(context)
    text_body = loader.get_template(
        'email_messages/workshop/create_workshop/message.txt').render(context)
    send_email_to_list(
        subject,
        body=email_body,
        users_list=all_email,
        text_body=text_body)
    success_url = reverse_lazy('workshops:workshop_list')
    return HttpResponseRedirect(success_url)


class WorkshopUpdate(views.LoginRequiredMixin, WorkshopAccessMixin,
                     generic.UpdateView):
    model = Workshop
    form_class = WorkshopEditForm
    template_name = 'workshops/workshop_update.html'

    def get_success_url(self):
        # pk = self.kwargs.get(self.pk_url_kwarg, None)
        self.success_url = reverse("workshops:workshop_list")
        return super(WorkshopUpdate, self).get_success_url()

    def get_initial(self):
        return {
            "requester": self.object.requester.name,
        }

    def get_form_kwargs(self):
        kwargs = super(WorkshopUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class WorkshopToggleActive(views.LoginRequiredMixin, views.CsrfExemptMixin,
                           views.JSONResponseMixin, WorkshopAccessMixin,
                           generic.UpdateView):
    model = Workshop
    fields = ('is_active', 'id')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.object.toggle_active(request.user, **kwargs)
        return self.render_json_response(response)


class WorkshopAction(views.CsrfExemptMixin, views.LoginRequiredMixin,
                     views.JSONResponseMixin, WorkshopEmailMixin,
                     generic.UpdateView):

    model = Workshop
    email_dir = 'email_messages/workshop/assign_me/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.object.manage_action(request.user, **kwargs)

        if response['status'] and response.get('notify') is not None:
            self.send_mail(request.user, response['assigned'])
            del response['notify']
        return self.render_json_response(response)

    def send_mail(self, user, assigned):
        """Send email to presenter and org users."""

        workshop = self.object
        context = {
            'presenter': True,
            'assigned': assigned,
            'date': workshop.expected_date,
            'presenter_name': user.username,
            'workshop_organization': workshop.requester,
            'workshop_url': self.request.build_absolute_uri(reverse(
                'workshops:workshop_detail', args=[workshop.pk]
            ))
        }
        # email to presenter and group
        self.send_mail_to_presenter(user, context)
        context['presenter'] = False
        self.send_mail_to_group(context, exclude_emails=[user.email])


class WorkshopFeedbackView(views.LoginRequiredMixin,
                           generic.FormView):
    form_class = WorkshopFeedbackForm
    template_name = "workshops/workshop_feedback.html"
    success_url = reverse_lazy('workshops:workshop_list')

    def form_valid(self, form):
        workshop_id = self.kwargs.get('pk')
        form.save(self.request.user, workshop_id)
        return super(WorkshopFeedbackView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(WorkshopFeedbackView, self).get_context_data(
            *args, **kwargs)
        context['workshop'] = Workshop.objects.get(pk=self.kwargs.get('pk'))
        return context


def upcoming_workshops(request):
    template_name = 'upcoming.html'
    workshop_list = Workshop.objects.filter(is_active=True).filter(
        status__in=[WorkshopStatus.REQUESTED,
            WorkshopStatus.ACCEPTED]).order_by('expected_date')
    for workshop in workshop_list:
        print(workshop.presenter)
    context_dict = {}
    context_dict['workshop_list'] = workshop_list

    return render(request, template_name, context_dict)
