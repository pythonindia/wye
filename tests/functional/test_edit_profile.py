import re

import pytest

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_signup_college_poc_flow(base_url, browser, outbox):
    f.create_usertype(slug='tutor', display_name='tutor')
    user = f.create_user()
    # user.set_password('123123')
    user.save()
    url = base_url + '/accounts/login/'
    browser.visit(url)
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    print(outbox)
    assert len(outbox) == 1
    mail = outbox[0]
    confirm_link = re.findall(r'http.*/accounts/.*/', mail.body)
    assert confirm_link
    browser.visit(confirm_link[0])
    assert browser.title, "Confirm E-mail Address"
    browser.find_by_css('[type=submit]')[0].click()

    assert "Login" in browser.title

    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present("My Profile")

    poc_type = f.create_usertype(slug='poc', display_name='College POC')
    user.profile.usertype.clear()
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

    # Use first name and last name
    browser.visit(url)
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    browser.visit(url)
    browser.fill('first_name', 'First Name')
    browser.fill('last_name', 'Last Name')
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.select('location', location1.id)
    assert browser.is_text_present('This field is required.')

    browser.visit(url)
    browser.fill('first_name', 'First Name')
    browser.fill('last_name', 'Last Name')
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.select('location', location1.id)
    browser.fill('occupation', 'occupation')
    browser.fill('work_location', 'work_location')
    browser.fill('work_experience', 'work_experience')

    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('Deactive Account')


def test_signup_tutor_flow(base_url, browser, outbox):
    tutor_type = f.create_usertype(slug='tutor', display_name='tutor')
    user = f.create_user()
    user.set_password('123123')
    user.save()
    url = base_url + '/accounts/login/'
    browser.visit(url)
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    assert len(outbox) == 1
    mail = outbox[0]
    confirm_link = re.findall(r'http.*/accounts/.*/', mail.body)
    assert confirm_link
    browser.visit(confirm_link[0])
    assert browser.title, "Confirm E-mail Address"
    browser.find_by_css('[type=submit]')[0].click()

    assert "Login" in browser.title

    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()

    assert browser.is_text_present("My Profile")

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

    browser.visit(url)
    browser.fill('first_name', 'First Name')
    browser.fill('last_name', 'Last Name')
    browser.fill('mobile', '1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_states', state1.id)
    browser.select('interested_level', 1)
    browser.select('location', location1.id)
    browser.fill('github', 'https://github.com')
    browser.fill('occupation', 'occupation')
    browser.fill('work_location', 'work_location')
    browser.fill('work_experience', 'work_experience')

    browser.find_by_css('[type=submit]')[0].click()
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
