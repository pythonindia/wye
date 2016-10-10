import re

import pytest

from .. import factories as f
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_signup_flow(base_url, browser, outbox):
    f.create_usertype(slug='tutor', display_name='tutor')
    # Sign-Up option should be present there
    browser.visit(base_url)
    sign_up_link = browser.find_by_text('Sign Up')[0]
    assert sign_up_link

    # On Clicking it, it should open a Sign Up Page
    sign_up_link.click()
    # asserting if it's the signup page or not
    assert 'Signup' in browser.title

    # Now Fill the relevant information

    browser.fill('first_name', 'random')
    browser.fill('last_name', 'person')
    browser.fill('mobile', '0812739120')
    browser.fill('username', 'randomnessprevails')
    browser.fill('email', 'random@a.com')
    browser.fill('password1', 'secretpassword')
    browser.fill('password2', 'secretpassword')

    # Click on the Submit Button
    browser.find_by_css('[type=submit]')[0].click()

    # Check for the text shown in the browser when user hits submit button
    assert browser.is_text_present(
        'We have sent an e-mail to you for verification')

    # Check for the mailbox for the confirmation link

    assert len(outbox) == 1
    mail = outbox[0]

    activate_link = re.findall(r'http.*/accounts/confirm-email/.*/', mail.body)
    assert activate_link

    browser.visit(activate_link[0])

    assert "Confirm E-mail Address" in browser.title
    browser.find_by_css('[type=submit]')[0].click()

    assert "Login" in browser.title

    browser.fill('login', 'random@a.com')
    browser.fill('password', 'secretpassword')
    browser.find_by_css('[type=submit]')[0].click()

    assert browser.is_text_present("Dashboard")

    u = User.objects.get(email='random@a.com')
    u.profile.usertype.clear()
    poc_type = f.create_usertype(slug='poc', display_name='College POC')
    u.profile.usertype.add(poc_type)
    section1 = f.create_workshop_section(name='section1')
    location1 = f.create_locaiton(name='location1')
    state1 = f.create_state(name='state1')

    url = base_url + '/profile/randomnessprevails/edit'
    browser.visit(url)

    # browser.select('usertype', poc_type.id)
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    #browser.select('interested_locations', location1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()

    assert browser.is_text_present('My Profile')
    assert browser.is_text_present('Graph')

    # Logging Out
    url = base_url + '/accounts/logout/'
    browser.visit(url)
    assert 'Home | PythonExpress' in browser.title
