from django.views import generic
from braces import views

from . import forms
from . import models


class RegionalLeadUpdate(views.LoginRequiredMixin, generic.CreateView):
    model = models.RegionalLead
    form_class = forms.RegionalLeadForm
