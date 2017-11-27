

import pytest
from .. import base
from .. import factories as f
from .. utils import create_user_verify_login
pytestmark = pytest.mark.django_db


def create_user_type(slug='tutor'):
    tutor_type = f.create_usertype(slug=slug, display_name=slug)
    return tutor_type


def test_signup_college_poc_flow(base_url, browser, outbox):
    create_user_type(slug='tutor')
    user = create_user_verify_login(base_url, browser, outbox)
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    # assert browser.is_text_present("My Profile")

    poc_type = f.create_usertype(slug='poc', display_name='College POC')
    user.profile.usertype.clear()
    user.profile.usertype.add(poc_type)
    user.profile.save()
    user.save()
    section1 = f.create_workshop_section(name='section1')

    location1 = f.create_locaiton(name='location1')
    state1 = f.create_state(name='state1')

    # mobile number chechk
    url = base_url + '/profile/' + user.username + '/edit/'
    browser.visit(url)
    browser.fill('mobile', '')
    browser.select('interested_sections', section1.id)
    browser.select('location', location1.id)
    browser.select('interested_states', state1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    # interested state check
    browser.fill('mobile', '1234567890')
    browser.select('location', location1.id)
    browser.select('interested_states', state1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    # location check
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    # Use first name and last name
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    # occupation is required
    browser.fill('first_name', 'First Name')
    browser.fill('last_name', 'Last Name')
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    # Sucess case
    browser = base.profile_poc_create(
        browser, url, None,
        section1.id, state1.id, location1.id)
    assert browser.is_text_present('Deactive Account')


def test_signup_tutor_flow(base_url, browser, outbox):
    tutor_type = create_user_type(slug='tutor')
    user = create_user_verify_login(base_url, browser, outbox)

    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()

    # assert browser.is_text_present("My Profile")
    poc_type = f.create_usertype(slug='poc', display_name='College POC')
    user.profile.usertype.clear()
    user.profile.usertype.add(tutor_type)
    user.profile.usertype.add(poc_type)
    user.profile.save()
    user.save()
    section1 = f.create_workshop_section(name='section1')
    location1 = f.create_locaiton(name='location1')
    state1 = f.create_state(name='state1')

    # mobile number chechk
    url = base_url + '/profile/' + user.username + '/edit'
    browser.visit(url)
    browser.fill('mobile', '')
    browser.select('usertype', tutor_type.id)
    browser.select('interested_sections', section1.id)
    browser.select('location', location1.id)
    browser.select('interested_states', state1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    # interested state check
    browser.visit(url)
    browser.fill('mobile', '1234567890')
    browser.select('location', location1.id)
    browser.select('interested_states', state1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    # location check
    browser.visit(url)
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    # Github check
    browser.visit(url)
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('Github or LinkedIn field is mandatory')

    browser.visit(url)
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.select('location', location1.id)
    browser.fill('github', 'https://github.com')
    browser.find_by_css('[type=submit]')[0].click()

    assert browser.is_text_present(
        'Interested workshop level field is mandatory')

    browser.visit(url)
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.select('interested_level', 1)
    browser.select('location', location1.id)
    browser.fill('github', 'https://github.com')
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    browser = base.profile_tutor_create(
        browser, url, tutor_type.id, section1.id, state1.id, location1.id)
    assert browser.is_text_present('Deactive Account')

    org = f.create_organisation(location=location1)
    org.user.add(user)
    # section2 = f.create_workshop_section(name='section2')

    w1 = f.create_workshop(requester=org, workshop_section=section1)
    w1.presenter.add(user)
    w2 = f.create_workshop(requester=org, workshop_section=section1)
    w2.presenter.add(user)
    w3 = f.create_workshop(requester=org, workshop_section=section1)
    w3.presenter.add(user)
    w4 = f.create_workshop(requester=org, workshop_section=section1)
    w4.presenter.add(user)
    w5 = f.create_workshop(requester=org, workshop_section=section1)
    w5.presenter.add(user)

    url = base_url + '/profile/' + user.username + '/'
    browser.visit(url)
    # assert browser.is_text_present('Deactive Account')
