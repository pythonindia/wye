from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from braces import views

from .forms import WorkshopForm, WorkshopFeedbackForm
from .mixins import WorkshopEmailMixin, WorkshopAccessMixin, \
    WorkshopFeedBackMixin, WorkshopRestrictMixin 
from .models import Workshop


class WorkshopList(views.LoginRequiredMixin, generic.ListView):
    model = Workshop
    template_name = 'workshops/workshop_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            WorkshopList, self).get_context_data(*args, **kwargs)
        workshop_list = Workshop.objects.all()
        context['workshop_list'] = workshop_list
        context['user'] = self.request.user
        return context


class WorkshopDetail(views.LoginRequiredMixin, generic.DetailView):
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
            'date': workshop.expected_date,
            'workshop_url': self.request.build_absolute_uri(reverse(
                'workshops:workshop_detail', args=[workshop.pk]
            ))
        }
        self.send_mail_to_group(context)
        return response


class WorkshopUpdate(views.LoginRequiredMixin, WorkshopAccessMixin, generic.UpdateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_update.html'

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        self.success_url = reverse(
            "workshops:workshop_update", args=[pk])
        return super(WorkshopUpdate, self).get_success_url()


class WorkshopToggleActive(views.LoginRequiredMixin, views.CsrfExemptMixin,
                           views.JSONResponseMixin, WorkshopAccessMixin, generic.UpdateView):
    model = Workshop

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.object.toggle_active(request.user, **kwargs)
        return self.render_json_response(response)


class WorkshopAssignMe(views.LoginRequiredMixin, views.CsrfExemptMixin,
                       views.JSONResponseMixin, WorkshopEmailMixin,
                       generic.UpdateView):
    model = Workshop
    email_dir = 'email_messages/workshop/assign_me/'

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


class WorkshopFeedbackView(views.LoginRequiredMixin, WorkshopFeedBackMixin,
                           generic.FormView):
    form_class = WorkshopFeedbackForm
    template_name = "workshops/workshop_feedback.html"
    success_url = reverse_lazy('workshops:workshop_list')

    def form_valid(self, form):
        workshop_id = self.kwargs.get('pk')
        form.save(self.request.user, workshop_id)
        return super(WorkshopFeedbackView, self).form_valid(form)
