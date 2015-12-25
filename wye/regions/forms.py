from django import forms
from django.core.exceptions import ValidationError

from wye.profiles.models import UserType

from . import models


class RegionalLeadForm(forms.ModelForm):

    class Meta:
        model = models.RegionalLead
        exclude = ()

    def clean(self):
        error_message = []
        if (self.cleaned_data.get('location', '') and
                self.cleaned_data.get('leads', '')):
            location = self.cleaned_data['location']
            for u in self.cleaned_data['leads']:
                if not u.profile:
                    error_message.append('Profile for user %s not found' % (u))
                elif u.profile.location != location:
                    error_message.append(
                        "User %s doesn't belong to region %s" % (u, location))
        if error_message:
            raise ValidationError(error_message)

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(RegionalLeadForm, self).save()
        for u in self.cleaned_data['leads']:
            u.profile.usertype.add(UserType.objects.get(slug='lead'))
        return m


class LocationForm(forms.ModelForm):

    class Meta:
        model = models.Location
        exclude = ()


class StateForm(forms.ModelForm):

    class Meta:
        model = models.State
        exclude = ()
