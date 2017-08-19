from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from simplemathcaptcha.fields import MathCaptchaField

from wye.base.constants import ContactFeedbackType

from . import models


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Email"), max_length=100, required=True)
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput,
                               required=True)


class SignupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        mandatory_field(self)

    mobile = forms.CharField(
        label=_("Mobile"),
        max_length=10,
        widget=forms.TextInput(
            attrs={'placeholder': 'Mobile'}
        )
    )

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        error_message = []
        if not mobile.isdigit():
            error_message.append(
                "Contact Number should only consist digits")
        if not len(mobile) == 10:
            error_message.append(
                "Contact Number should be of 10 digits")

        if error_message:
            raise ValidationError(error_message)
        return mobile

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'First Name', 'autofocus': 'on'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Last Name'}),
        }

    def signup(self, request, user):
        profile = user.profile
        profile.mobile = self.cleaned_data['mobile']
        profile.save()


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", max_length=50)
    last_name = forms.CharField(label="Last Name", max_length=50)
    queryset = models.UserType.objects.exclude(
        slug__in=['admin', 'lead', 'coordinator'])
    usertype = forms.ModelMultipleChoiceField(
        label="Usertype", queryset=queryset)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].required = True
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['occupation'].required = True
        mandatory_field(self)

    def clean_interested_states(self):
        if ('tutor' in [u.slug for u in self.cleaned_data['usertype']]):
            if not self.cleaned_data['interested_states']:
                raise ValidationError('States field is mandatory')
        return self.cleaned_data['interested_states']

    def clean_github(self):
        if ('tutor' in [u.slug for u in self.cleaned_data['usertype']]):
            if not(
                ('github' in self.cleaned_data and
                    self.cleaned_data['github']) or
                ('linkedin' in self.cleaned_data and
                    self.cleaned_data['linkedin'])
            ):
                raise ValidationError(
                    'Github or LinkedIn field is mandatory')
        return self.cleaned_data['github']

    def clean_linkedin(self):
        if ('tutor' in [u.slug for u in self.cleaned_data['usertype']]):
            if not (
                ('github' in self.cleaned_data and
                    self.cleaned_data['github']) or
                ('linkedin' in self.cleaned_data and
                    self.cleaned_data['linkedin'])
            ):
                raise ValidationError(
                    'Github or LinkedIn field is mandatory')
        return self.cleaned_data['linkedin']

    def clean_interested_level(self):
        if ('tutor' in [u.slug for u in self.cleaned_data['usertype']]):
            if not self.cleaned_data['interested_level']:
                raise ValidationError(
                    'Interested workshop level field is mandatory')
        return self.cleaned_data['interested_level']

    def is_valid(self):
        return super(UserProfileForm, self).is_valid()

    def save(self, *args, **kwargs):
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.save()
        profile_form = super(UserProfileForm, self).save(commit=True)
        return profile_form

    class Meta:
        model = models.Profile
        exclude = ('user', 'slug', 'interested_locations')
        fields = (
            'first_name', 'last_name', 'mobile',
            'picture',
            'occupation', 'work_location',
            'work_experience', 'no_workshop', 'is_mobile_visible',
            'is_email_visible', 'enable_notifications', 'usertype',
            'interested_sections', 'interested_level', 'interested_states',
            'location', 'github', 'facebook', 'googleplus',
            'linkedin', 'twitter', 'slideshare')


class ContactUsForm(forms.Form):

    name = forms.CharField(label='Your name*', required=True)
    email = forms.EmailField(label='Your email*', required=True)
    feedback_type = forms.ChoiceField(label='Feedback on*', required=True,
                                      choices=ContactFeedbackType.CHOICES)
    comments = forms.CharField(
        label='Comments*', required=True, widget=forms.Textarea)
    contact_number = forms.CharField(
        label='Your contact number', required=False)
    captcha = MathCaptchaField()

    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        error_message = []
        if not contact_number.isdigit():
            error_message.append(
                "Contact Number should only consist digits")
        if not len(contact_number) == 10:
            error_message.append(
                "Contact Number should be of 10 digits")

        if error_message:
            raise ValidationError(error_message)
        return contact_number


def mandatory_field(self):
    for v in filter(lambda x: x.required, self.fields.values()):
        v.label = str(v.label) + "*"


class PartnerForm(forms.Form):
    partner_choices = (
        ('profit', 'Profit making'),
        ('non-profit', "Non Profit"))
    org_name = forms.CharField(label='Organization Name*', required=True)
    org_url = forms.URLField(label='Organization Url*', required=True)
    partner_type = forms.ChoiceField(
        label='Type of organization*',
        required=True, choices=partner_choices)
    description = forms.CharField(
        label='Describe how your organization will help both of us *',
        required=True, widget=forms.Textarea)
    python_use = forms.CharField(
        label='Use of python in your organization ? *',
        required=True, widget=forms.Textarea)
    name = forms.CharField(label='Your Name*', required=True)
    email = forms.EmailField(label='Your email*', required=True)
    contact_number = forms.CharField(
        label='Your contact number', required=True)

    comments = forms.CharField(
        label='Comments*',
        required=True, widget=forms.Textarea)

    captcha = MathCaptchaField()

    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        error_message = []
        if not contact_number.isdigit():
            error_message.append(
                "Contact Number should only consist digits")
        if not len(contact_number) == 10:
            error_message.append(
                "Contact Number should be of 10 digits")

        if error_message:
            raise ValidationError(error_message)
        return contact_number
