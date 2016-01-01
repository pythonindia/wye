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
        try:
            self.fields['email'].label = "E-mail*"
            self.fields['username'].label = "Username*"
            self.fields['password1'].label = "Password*"
            self.fields['password2'].label = "Password (again)*"
        except:
            pass

    mobile = forms.CharField(
        label=_("Mobile*"),
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
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'autofocus': 'on'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        }

    def signup(self, request, user):
        profile = user.profile
        profile.mobile = self.cleaned_data['mobile']
        profile.save()


class UserProfileForm(forms.ModelForm):

    usertype = forms.ModelMultipleChoiceField(
        queryset=models.UserType.objects.exclude(slug__in=['admin', 'lead']))

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Profile
        exclude = ('user', 'slug')


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
