import re
from tests import factories as f

from wye.base.constants import WorkshopLevel
outbox_len = 0


def create_user(password):
    user = f.create_user()
    user.set_password(password)
    user.save()
    return user


def login(browser, url, user, password):
    browser.visit(url)
    browser.fill('login', user.email)
    browser.fill('password', password)
    browser.find_by_css('[type=submit]')[0].click()


def login_and_confirm(browser, url, outbox, user, password):
    global outbox_len
    outbox_len = outbox_len + 1
    browser.visit(url)
    browser.fill('login', user.email)
    browser.fill('password', password)
    browser.find_by_css('[type=submit]')[0].click()
#     assert len(outbox) == outbox_len
    mail = outbox[len(outbox) - 1]
    confirm_link = re.findall(r'http.*/accounts/.*/', mail.body)
    assert confirm_link
    browser.visit(confirm_link[0])
    assert browser.title, "Confirm E-mail Address"
    browser.find_by_css('[type=submit]')[0].click()


def workshop_create(browser, url, org, section):
    browser.visit(url)
    browser.select('no_of_participants', 10)
    browser.fill('expected_date', '11/12/2018')
    browser.fill('description', "test")
    browser.select('requester', org.id)
    browser.select('workshop_level', WorkshopLevel.BEGINNER)
    browser.select('workshop_section', section.id)
    browser.find_by_css('[type=submit]')[0].click()


def profile_poc_create(
        browser, url, usertype_id,
        section_id, state_id, location_id):
    browser.visit(url)
    browser.fill('first_name', 'First Name')
    browser.fill('last_name', 'Last Name')
    browser.fill('mobile', '1234567890')
    browser.fill('occupation', 'occupation')
    browser.fill('work_location', 'work_location')
    browser.fill('work_experience', 1)
    if usertype_id:
        browser.select('usertype', usertype_id)
    browser.select('interested_sections', section_id)
    browser.select('interested_states', state_id)
    browser.select('location', location_id)
    browser.find_by_css('[type=submit]')[0].click()
    return browser


def profile_tutor_create(
        browser, url, usertype_id,
        section_id, state_id, location_id):
    browser.visit(url)
    browser.fill('first_name', 'First Name')
    browser.fill('last_name', 'Last Name')
    browser.fill('mobile', '1234567890')
    browser.select('usertype', usertype_id)
    browser.select('interested_sections', section_id)
    browser.select('interested_states', state_id)
    browser.select('interested_level', 1)
    browser.select('location', location_id)
    browser.fill('github', 'https://github.com')
    browser.fill('occupation', 'occupation')
    browser.fill('work_location', 'work_location')
    browser.fill('work_experience', 1)
    browser.find_by_css('[type=submit]')[0].click()
    return browser
