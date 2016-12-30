import datetime

from django import forms
from django.conf import settings
# from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from wye.base.constants import (
    WorkshopRatings,
    WorkshopLevel,
    WorkshopStatus,
    FeedbackType)
from wye.base.widgets import CalendarWidget
from wye.organisations.models import Organisation
from wye.profiles.models import Profile
from wye.regions.models import RegionalLead, Location, State

from .models import (
    Workshop,
    WorkshopRatingValues,
    WorkshopFeedBack,
    WorkshopSections)


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

    # def clean_location(self):
    #     if "requester" not in self.cleaned_data:
    #         return ""

    #     organisation = self.cleaned_data['requester']
    #     return organisation.location

    def get_organisations(self, user):
        if Profile.is_admin(user):
            return Organisation.objects.all()
        elif Profile.is_regional_lead(user):
            return Organisation.objects.filter(location=user.profile.location)
        else:
            return Organisation.list_user_organisations(user)

    def clean_expected_date(self):
        date = self.cleaned_data['expected_date']
        if not (date > datetime.date.today() + datetime.timedelta(days=14)):
            raise ValidationError(
                '''Workshop request has to future date and
                 atleast 2 weeks ahead of today''')
        else:
            return date

    def clean_location(self):
        # data = self.cleaned_data['requester']
        if ('requester' not in self.data) or (not self.data['requester']):
            return None
        o = Organisation.objects.get(id=self.data['requester'])
        return o.location

    class Meta:
        model = Workshop
        exclude = (
            'presenter', 'created_at', 'modified_at',
            'is_active', 'status',)


class WorkshopEditForm(forms.ModelForm):
    requester = forms.CharField()

    def __init__(self, request, *args, **kwargs):
        super(WorkshopEditForm, self).__init__(*args, **kwargs)
        self.fields['expected_date'] = forms.DateField(
            widget=CalendarWidget,
            input_formats=settings.ALLOWED_DATE_FORMAT)
        self.fields['requester'].widget = forms.TextInput()
        self.fields['requester'].widget.attrs['readonly'] = True
        if RegionalLead.is_regional_lead(
                request.user, self.instance.location):
            self.fields['presenter'].queryset = User.objects.filter(
                profile__usertype__slug="tutor"
            )
        else:
            del self.fields['presenter']

    def clean_requester(self):
        return self.instance.requester

    class Meta:
        model = Workshop
        exclude = (
            'created_at', 'modified_at', 'is_active',
            'status', 'location')


class WorkshopFeedbackForm(forms.Form):
    """
    Dynamically generates feedback form depending on questions available
    in model assigend to question_model.
    """

    question_model = WorkshopRatingValues

    def __init__(self, user, id, *args, **kwargs):
        super(WorkshopFeedbackForm, self).__init__(*args, **kwargs)
        w = Workshop.objects.get(id=id)
        if user in w.presenter.all():
            feedback_type = FeedbackType.PRESENTER
        elif user in w.requester.user.all():
            feedback_type = FeedbackType.ORGANISATION
        else:
            feedback_type = None
        questions = self.question_model.get_questions(feedback_type)

        for question in questions:
            key = "{}".format(question)
            self.fields[key] = forms.ChoiceField(
                choices=WorkshopRatings.CHOICES, required=True,
                widget=forms.RadioSelect())
            self.fields[key].label = question.name

        self.fields["comment"] = forms.CharField(widget=forms.Textarea)

    def save(self, user, workshop_id):
        print(dir(self))
        data = {k: v for k, v in self.cleaned_data.items()}
        WorkshopFeedBack.save_feedback(user, workshop_id, **data)


class WorkshopListForm(forms.Form):
    """
    Form to filter workshop list
    """
    state = forms.ModelMultipleChoiceField(
        label="Workshop Location",
        required=False,
        queryset='')

    presenter = forms.ModelMultipleChoiceField(
        label="Presenter",
        required=False,
        queryset='')

    level = forms.MultipleChoiceField(
        label="Level",
        required=False,
        choices=WorkshopLevel.CHOICES)

    section = forms.ModelMultipleChoiceField(
        label="Section",
        required=False,
        queryset='')

    status = forms.MultipleChoiceField(
        label="Status",
        required=False,
        choices=WorkshopStatus.CHOICES)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(WorkshopListForm, self).__init__(*args, **kwargs)
        self.fields['state'].queryset = self.get_all_locations(user)
        if Profile.is_admin(user) or Profile.is_regional_lead(user):
            self.fields['presenter'].queryset = User.objects.filter(
                profile__usertype__slug="tutor"
            )
        elif 'poc' in user.profile.get_user_type:
            self.fields['presenter'].queryset = User.objects.filter(
                profile__usertype__slug="tutor",
                profile__location__state__in=self.get_all_states(user)
            )
        else:
            del self.fields['presenter']
        self.fields['section'].queryset = WorkshopSections.objects.all()

    def get_all_locations(self, user):
        if Profile.is_admin(user):
            return Location.objects.all()
        else:
            return user.profile.interested_locations.all()

    def get_all_states(self, user):
        if Profile.is_admin(user):
            return State.objects.all()
        else:
            return user.profile.interested_states.all()
