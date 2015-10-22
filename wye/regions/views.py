from django.views import generic
from braces import views

from . import forms
from . import models


class RegionalLeadList(views.LoginRequiredMixin, generic.CreateView):
    model = models.RegionalLead
    form_class = forms.RegionalLeadForm
    template_name = 'regions/list.html'
