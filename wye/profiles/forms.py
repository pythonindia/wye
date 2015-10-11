from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from wye.workshops.models import WorkshopSections
from wye.regions.models import Location
from . import models


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Email"), max_length=100, required=True)
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput,
                               required=True)


class SignupForm(forms.ModelForm):
    mobile = forms.CharField(
        label=_("Mobile"),
        max_length=10,
        widget=forms.TextInput(
            attrs={'placeholder': 'Mobile'}
        )
    )
    usertype = forms.ModelMultipleChoiceField(
        queryset=models.UserType.objects.exclude(slug='admin'))
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    interested_locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all())
    interested_sections = forms.ModelMultipleChoiceField(
        queryset=WorkshopSections.objects.all())

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
        profile.location = self.cleaned_data['location']
        profile.usertype = self.cleaned_data['usertype']
        profile.interested_locations = self.cleaned_data['interested_locations']
        profile.interested_sections = self.cleaned_data['interested_sections']
        profile.save()
        user.save()


class UserProfileForm(forms.ModelForm):

    usertype = forms.ModelMultipleChoiceField(
        queryset=models.UserType.objects.exclude(slug='admin'))

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Profile
        exclude = ('user', 'slug')
