from django import forms
from django.conf import settings
from .models import Workshop


class WorkshopForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkshopForm, self).__init__(*args, **kwargs)
        self.fields['expected_date'] = forms.DateField(
            input_formats=settings.ALLOWED_DATE_FORMAT)

    class Meta:
        model = Workshop
        exclude = (
            'presenter', 'created_at', 'modified_at', 
            'is_active', 'status')
