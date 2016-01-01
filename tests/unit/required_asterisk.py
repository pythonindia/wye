from wye.profiles.forms import UserProfileForm
from wye.profiles.forms import SignupForm


def test_edit_profile():
    userprofileform = UserProfileForm(auto_id=False)
    for field in userprofileform.fields.values():
        if (field.required):
            assert field.label.endswith("*")


def test_signup_form():
    signupform = SignupForm(auto_id=False)
    for field in signupform.fields.values():
        if (field.required):
            assert field.label.endswith("*")
