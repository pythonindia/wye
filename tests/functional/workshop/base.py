import re
from tests import factories as f


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
    assert len(outbox) == outbox_len
    mail = outbox[outbox_len - 1]
    confirm_link = re.findall(r'http.*/accounts/.*/', mail.body)
    assert confirm_link
    browser.visit(confirm_link[0])
    assert browser.title, "Confirm E-mail Address"
    browser.find_by_css('[type=submit]')[0].click()
