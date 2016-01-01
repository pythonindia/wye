import re

import pytest

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_signup_flow(base_url, browser, outbox):

    user = f.create_user()
    user.set_password('123123')
    user.save()
    url = base_url + '/workshop/'
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

    assert browser.is_text_present("Edit Profile")

    poc_type = f.create_usertype(slug='dummy', display_name='College POC')
    section1 = f.create_workshop_section(name='section1')
    location1 = f.create_locaiton(name='location1')

    #mobile number chechk
    url = base_url + '/profile/'+user.username+'/edit'
    browser.visit(url)
    browser.fill('mobile','')
    browser.select('usertype', poc_type.id)
    browser.select('interested_sections', section1.id)
    browser.select('interested_locations', location1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    #usertype check
    browser.visit(url)
    browser.fill('mobile','1234567890')
    browser.select('interested_sections', section1.id)
    browser.select('interested_locations', location1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    #intrested_location chechk
    url = base_url + '/profile/'+user.username+'/edit'
    browser.visit(url)
    browser.fill('mobile','1234567890')
    browser.select('usertype', poc_type.id)
    browser.select('interested_locations', location1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    #intrested location chechk
    url = base_url + '/profile/'+user.username+'/edit'
    browser.visit(url)
    browser.fill('mobile','')
    browser.select('usertype', poc_type.id)
    browser.select('interested_sections', section1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    #location chechk
    url = base_url + '/profile/'+user.username+'/edit'
    browser.visit(url)
    browser.fill('mobile','')
    browser.select('usertype', poc_type.id)
    browser.select('interested_sections', section1.id)
    browser.select('interested_locations', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')