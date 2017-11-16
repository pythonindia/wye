from django import forms
from .models import Organisation, User


class OrganisationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganisationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organisation
        exclude = ('user', 'created_at', 'modified_at',
                   'active', 'created_by', 'modified_by')


class OrganisationMemberAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganisationMemberAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organisation
        exclude = ('user', 'created_at', 'modified_at',
                   'name', 'organisation_type', 'description',
                   'location', 'organisation_role',
                   'active', 'created_by', 'modified_by')

    existing_user = forms.ModelChoiceField(
        queryset=User.objects.all(), required=False)
    new_user = forms.EmailField(label='Invite New User', required=False)

    def clean(self):
        user = self.cleaned_data.get('existing_user')
        new_user = self.cleaned_data['new_user']

        if not (user or new_user):
            raise forms.ValidationError(
                'Please choose existing user or add new user')
        return self.cleaned_data


class UserRegistrationForm(forms.ModelForm):
    """
    Form class for completing a user's registration and activating the
    User.

    The class operates on a user model which is assumed to have the required
    fields of a BaseUserModel
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=30,
                                       widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.initial['username'] = ''

    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'is_active', 'last_login',
                   'date_joined', 'groups', 'user_permissions')
