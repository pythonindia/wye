from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from braces import views
from .models import Workshop
from .forms import WorkshopForm


class WorkshopList(generic.ListView):
    model = Workshop
    context_object_name = 'workshop_list'
    template_name = 'workshops/workshop_list.html'


class WorkshopDetail(generic.DetailView):
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


class WorkshopToggleActive(views.LoginRequiredMixin,
    views.CsrfExemptMixin, views.JSONResponseMixin,
    generic.View):
    model = Workshop

    def post(self, request, *args, **kwargs):
        response = self.model.toggle_active(**kwargs)
        return self.render_json_response(response)


class WorkshopAssignMe(views.LoginRequiredMixin,
     views.CsrfExemptMixin, views.JSONResponseMixin,
     generic.View):
     model = Workshop

