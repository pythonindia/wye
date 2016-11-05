import re
from tests import factories as f

from wye.base.constants import WorkshopLevel
outbox_len = 0


def create_user(password):
    user = f.create_user()
    user.set_password(password)
    user.save()
    user.first_name = user.username
    user.last_name = user.username
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
    browser.fill('no_of_participants', 10)
    browser.fill('expected_date', '11/12/2018')
    browser.fill('description', "test")
    browser.select('requester', org.id)
    browser.select('workshop_level', WorkshopLevel.BEGINNER)
    browser.select('workshop_section', section.id)
    browser.find_by_css('[type=submit]')[0].click()
