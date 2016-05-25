from django import forms

# import autocomplete_light

from .models import Organisation, User


class OrganisationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganisationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organisation
        exclude = ('user', 'created_at', 'modified_at',
                   'active', 'created_by', 'modified_by')
#         widgets = {
#             'name': autocomplete_light.TextWidget('OrganisationAutocomplete'),
#         }


class OrganisationMemberAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganisationMemberAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organisation
        exclude = ('user', 'created_at', 'modified_at',
                   'name', 'organisation_type', 'description',
                   'location', 'organisation_role',
                   'active', 'created_by', 'modified_by')

    users = User.objects.values_list('id', 'username')
    user_choices = [('', '----------')] + [(id, username) for (id, username) in users]
    existing_user = forms.ChoiceField(user_choices, required=False)
    new_user = forms.EmailField(label='Invite New User', required=False)


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
