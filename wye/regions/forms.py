from django import forms

from . import models


class RegionalLeadForm(forms.ModelForm):

    class Meta:
        model = models.RegionalLead
        fields = ('location', 'leads')
