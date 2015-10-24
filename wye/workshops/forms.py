from django import forms
from django.conf import settings

from wye.base.widgets import CalendarWidget

from django.utils.text import slugify
from .models import Workshop, WorkshopRatingValues


class WorkshopForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkshopForm, self).__init__(*args, **kwargs)
        self.fields['expected_date'] = forms.DateField(
            widget=CalendarWidget,
            input_formats=settings.ALLOWED_DATE_FORMAT)

    class Meta:
        model = Workshop
        exclude = (
            'presenter', 'created_at', 'modified_at',
            'is_active')


class WorkshopFeedback(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = WorkshopRatingValues.get_questions()

        for question in questions:
            self.fields[slugify(question)] = forms.TextField()

