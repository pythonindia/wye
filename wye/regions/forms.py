from django import forms
import autocomplete_light

from . import models


class RegionalLeadForm(forms.ModelForm):

    class Meta:
        model = models.RegionalLead
        fields = ('location', 'leads')
    widgets = {
        'user': autocomplete_light.TextWidget('RegionalLeadAutocomplete'),
    }
