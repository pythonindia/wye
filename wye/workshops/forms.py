from django import forms
from django.conf import settings
from django.utils.text import slugify

from wye.base.widgets import CalendarWidget
from wye.base.constants import WorkshopRatings

from .models import Workshop, WorkshopRatingValues, WorkshopFeedBack


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


class WorkshopFeedbackForm(forms.Form):
    """
    Dynamically generates feedback form depending on questions available
    in model assigend to question_model.
    """

    question_model = WorkshopRatingValues

    def __init__(self, *args, **kwargs):
        super(WorkshopFeedbackForm, self).__init__(*args, **kwargs)
        questions = self.question_model.get_questions()

        for question in questions:
            key = "{}-{}".format(
                slugify(question["name"]), question["pk"]
            )
            self.fields[key] = forms.ChoiceField(
                choices=WorkshopRatings.CHOICES, required=True,
                widget=forms.RadioSelect())
            self.fields[key].label = question["name"]

        self.fields["comment"] = forms.CharField(widget=forms.Textarea)

    def save(self, user, workshop_id):
        data = {k.split("-")[-1]: v for k, v in self.cleaned_data.iteritems()}
        WorkshopFeedBack.save_feedback(user, workshop_id, **data)
