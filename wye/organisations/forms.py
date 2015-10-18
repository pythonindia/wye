from django import forms
from django.conf import settings
from .models import Organisation


class OrganisationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganisationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organisation
        exclude = ('user', 'created_at', 'modified_at', 'active')
