from django import forms

from . import models


class RegionalLeadForm(forms.ModelForm):

    class Meta:
        model = models.RegionalLead
        exclude = ()


class LocationForm(forms.ModelForm):

    class Meta:
        model = models.Location
        exclude = ()


class StateForm(forms.ModelForm):

    class Meta:
        model = models.State
        exclude = ()
