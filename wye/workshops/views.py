from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from braces import views
from wye.base.emailer import send_mail
#from wye.organisations.models import Organisation
from wye.profiles.models import Profile

from .forms import WorkshopForm
from .models import Workshop


class WorkshopList(views.LoginRequiredMixin, generic.ListView):
    model = Workshop
    template_name = 'workshops/workshop_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            WorkshopList, self).get_context_data(*args, **kwargs)
        workshop_list = Workshop.objects.filter()
        # organisation_list = Organisation.objects.filter(
        #                user=self.request.user)
        context['workshop_list'] = workshop_list
        context['workshop_feedback_pending'] = []
        context['workshop_in_queue'] = []
        context['workshop_completed'] = []
        context['workshop_withdrawn'] = []
        context['user'] = self.request.user
        return context


class WorkshopDetail(views.LoginRequiredMixin, generic.DetailView):
    model = Workshop
    context_object_name = "workshop"
    template_name = 'workshops/workshop_list.html'


class WorkshopCreate(views.LoginRequiredMixin, generic.CreateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_create.html'
    success_url = reverse_lazy('workshops:workshop_list')


class WorkshopUpdate(views.LoginRequiredMixin, generic.UpdateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_update.html'

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        self.success_url = reverse(
            "workshops:workshop_update", args=[pk])
        return super(WorkshopUpdate, self).get_success_url()


class WorkshopToggleActive(views.LoginRequiredMixin, views.CsrfExemptMixin,
                           views.JSONResponseMixin, generic.UpdateView):
    model = Workshop

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.object.toggle_active(request.user, **kwargs)
        return self.render_json_response(response)


class WorkshopAssignMe(views.LoginRequiredMixin, views.CsrfExemptMixin,
                       views.JSONResponseMixin, generic.UpdateView):
    model = Workshop

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        response = self.object.assign_me(user, **kwargs)
        if response['status']:
            self.send_mail(user, response['assigned'])
        return self.render_json_response(response)

    def send_mail(self, user, assigned):
        """Send email to presenter and org users."""

        workshop = self.object
        email_dir = 'workshops/email/assign_me/'
        last_presenter = user
        # Collage POC and admin email
        poc_admin_user = Profile.get_user_with_type(
            user_type=['Collage POC', 'admin']
        ).values_list('email', flat=True)
        # Org user email
        org_user_emails = workshop.requester.user.filter(
            is_active=True
        ).values_list('email', flat=True)
        # all presenter except current assigned presenter
        all_presenter_email = workshop.presenter.exclude(
            pk=last_presenter.pk
        ).values_list(
            'email', flat=True
        )
        context = {
            'presenter': True,
            'assigned': assigned,
            'date': workshop.expected_date,
            'presenter_name': last_presenter.username,
            'workshop_organization': workshop.requester,
            'workshop_url': self.request.build_absolute_uri(reverse(
                'workshops:workshop_detail', args=[workshop.pk]
            ))
        }
        # Send email to presenter
        send_mail([last_presenter.email], context, email_dir)
        # Send email to org users and other presenter(s).
        context['presenter'] = False
        all_email = []
        all_email.extend(org_user_emails)
        all_email.extend(all_presenter_email)
        all_email.extend(poc_admin_user)
        all_email = list(set(all_email))
        send_mail(all_email, context, email_dir)
