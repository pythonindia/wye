from django import forms

import autocomplete_light

from .models import Organisation


class OrganisationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganisationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organisation
        exclude = ('user', 'created_at', 'modified_at',
                   'active', 'created_by', 'modified_by')
        widgets = {
            'name': autocomplete_light.TextWidget('OrganisationAutocomplete'),
        }
