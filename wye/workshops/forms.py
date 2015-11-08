from django import forms
from django.conf import settings
from django.utils.text import slugify

from wye.base.constants import WorkshopRatings
from wye.base.widgets import CalendarWidget
from wye.organisations.models import Organisation
from wye.profiles.models import Profile

from .models import Workshop, WorkshopRatingValues, WorkshopFeedBack


class WorkshopForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(WorkshopForm, self).__init__(*args, **kwargs)
        self.fields['expected_date'] = forms.DateField(
            widget=CalendarWidget,
            input_formats=settings.ALLOWED_DATE_FORMAT)
        self.fields['requester'].queryset = self.get_organisations(user)
        self.fields['location'].required = False
        self.fields['location'].widget = forms.HiddenInput()

    def clean_location(self):
        if "requester" not in self.cleaned_data:
            return ""

        organisation = self.cleaned_data['requester']
        return organisation.location

    def get_organisations(self, user):
        if Profile.is_admin(user):
            return Organisation.objects.all()
        elif Profile.is_regional_lead(user):
            return Organisation.objects.filter(location=user.profile.location)
        else:
            return Organisation.list_user_organisations(user)

    class Meta:
        model = Workshop
        exclude = (
            'presenter', 'created_at', 'modified_at',
            'is_active', 'status',)


class WorkshopEditForm(forms.ModelForm):
    requester = forms.CharField()

    def __init__(self, *args, **kwargs):

        super(WorkshopEditForm, self).__init__(*args, **kwargs)
        self.fields['expected_date'] = forms.DateField(
            widget=CalendarWidget,
            input_formats=settings.ALLOWED_DATE_FORMAT)
        self.fields['requester'].widget = forms.TextInput()
        self.fields['requester'].widget.attrs['readonly'] = True

    def clean_requester(self):
        return self.instance.requester

    class Meta:
        model = Workshop
        exclude = (
            'presenter', 'created_at', 'modified_at',
            'is_active', 'status', 'location')


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
        data = {k.split("-")[-1]: v for k, v in self.cleaned_data.items()}
        WorkshopFeedBack.save_feedback(user, workshop_id, **data)
