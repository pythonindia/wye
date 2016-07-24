from wye.profiles.forms import SignupForm


def test_invalid_mobile_number1():
    mobile = SignupForm({'mobile': '123$%78@0j'})
    mobile.is_valid()
    assert "Contact Number should only consist digits" in (
        mobile.errors['mobile'])


def test_invalid_mobile_number2():
    mobile = SignupForm({'mobile': '12345'})
    mobile.is_valid()
    assert "Contact Number should be of 10 digits" in (mobile.errors['mobile'])
