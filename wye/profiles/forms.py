from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from . import models


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Email"), max_length=100, required=True)
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput,
                               required=True)


class SignupForm(UserCreationForm):
    '''
    '''
    username = forms.CharField(label=_("Email"), max_length=100, required=True)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput,
                                required=True)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))
    firstname = forms.CharField(label=_("First Name"), max_length=150,
                                required=True)
    lastname = forms.CharField(label=_("Last Name"), max_length=150,
                               required=True)

    mobile = forms.CharField(label=_("Mobile"), max_length=10,
                             required=True)


class UserProfile(forms.ModelForm):
    model = models.Profile
