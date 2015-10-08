from django.views import generic
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
    template_name = 'workshops/workshop_list.html'


class WorkshopUpdate(generic.UpdateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_list.html'


class WorkshopDelete(generic.DeleteView):
    model = Workshop
    template_name = 'workshops/workshop_list.html'
