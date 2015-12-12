from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import generic

from braces import views
from wye.profiles.models import Profile
from wye.regions.models import RegionalLead
from wye.social.sites.twitter import send_tweet

from .forms import WorkshopForm, WorkshopEditForm, WorkshopFeedbackForm
from .mixins import WorkshopEmailMixin, WorkshopAccessMixin, \
    WorkshopRestrictMixin
from .models import Workshop


class WorkshopList(views.LoginRequiredMixin, generic.ListView):
    model = Workshop
    template_name = 'workshops/workshop_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user_profile, created = Profile.objects.get_or_create(
            user__id=self.request.user.id)
        if not user_profile.get_user_type:
            return redirect('profiles:profile-edit', slug=request.user.username)
        return super(WorkshopList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            WorkshopList, self).get_context_data(*args, **kwargs)
        workshop_list = Workshop.objects.all()
        if Profile.is_organiser(self.request.user):
            workshop_list = workshop_list.filter(
                requester__user=self.request.user)
        elif Profile.is_presenter(self.request.user):
            workshop_list = workshop_list.filter(
                Q(presenter=self.request.user) | Q
                (requester__location__id__in=[
                    x.id for x in
                    self.request.user.profile.interested_locations.all()]))
        elif Profile.is_regional_lead(self.request.user):
            regions = RegionalLead.objects.filter(leads=self.request.user)
            workshop_list = workshop_list.filter(
                location__id__in=[x.location.id for x in regions])

        context['workshop_list'] = workshop_list
        context['user'] = self.request.user
        # need to improve the part
        context['is_not_tutor'] = False
        # as user can be tutor and regional lead hence we need to verify like
        # this
        if (Profile.is_regional_lead(self.request.user) or
                Profile.is_organiser(self.request.user) or
                Profile.is_admin(self.request.user)):
            context['is_not_tutor'] = True
        return context


class WorkshopDetail(generic.DetailView):
    model = Workshop
    context_object_name = "workshop"
    template_name = 'workshops/workshop_detail.html'


class WorkshopCreate(views.LoginRequiredMixin, WorkshopRestrictMixin,
                     WorkshopEmailMixin, generic.CreateView):
    model = Workshop
    email_dir = 'email_messages/workshop/create_workshop/'
    form_class = WorkshopForm
    template_name = 'workshops/workshop_create.html'
    success_url = reverse_lazy('workshops:workshop_list')

    def form_valid(self, form):
        response = super(WorkshopCreate, self).form_valid(form)
        workshop = self.object
        context = {
            'workshop': workshop,
            'date': workshop.expected_date,
            'workshop_url': self.request.build_absolute_uri(reverse(
                'workshops:workshop_detail', args=[workshop.pk]
            ))
        }
        send_tweet(context)
        self.send_mail_to_group(context)
        return response

    def get_form_kwargs(self):
        kwargs = super(WorkshopCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


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
