from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
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


class WorkshopCreate(generic.CreateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_create.html'
    success_url = reverse_lazy('workshops:workshop_list')


class WorkshopUpdate(generic.UpdateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_update.html'

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        self.success_url = reverse(
            "workshops:workshop_update", args=[pk])
        return super(WorkshopUpdate, self).get_success_url()

class WorkshopDelete(generic.DeleteView):
    model = Workshop
    context_object_name = "workshop"
    template_name = 'workshops/workshop_confirm_delete.html'
    success_url = reverse_lazy('workshops:workshop_list')
