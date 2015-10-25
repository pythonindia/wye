from django import forms
from django.conf import settings

from wye.base.widgets import CalendarWidget

from . import models


class WorkshopForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkshopForm, self).__init__(*args, **kwargs)
        self.fields['expected_date'] = forms.DateField(
            widget=CalendarWidget,
            input_formats=settings.ALLOWED_DATE_FORMAT)

    class Meta:
        model = models.Workshop
        exclude = (
            'presenter', 'created_at', 'modified_at',
            'is_active')


class WorkshopFeedBackForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkshopFeedBackForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.WorkshopFeedBack
        exclude = ('workshop',)
