import re
from .. import factories as f


def test_profile_flow(base_url, browser, outbox):
    user = f.create_user(username='profile1')
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

    url = base_url + '/accounts/login/'
    browser.visit(url)
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()

    poc_type = f.create_usertype(slug='dummy', display_name='College POC')
    section1 = f.create_workshop_section(name='section1')
    location1 = f.create_locaiton(name='location1')
    url = base_url + '/profile/{}/'.format(user.username)
    browser.visit(url)

    url = base_url + '/profile/{}/edit'.format(user.username)
    browser.visit(url)
    browser.fill('mobile', "1234567890")
    browser.select('usertype', poc_type.id)
    browser.select('interested_sections', section1.id)
    browser.select('interested_locations', location1.id)
    browser.select('location', location1.id)
    browser.find_by_css('[type=submit]')[0].click()
