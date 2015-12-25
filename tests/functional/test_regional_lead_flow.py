import pdb
import re
from .. import factories as f


def test_regional_lead_flow(base_url, browser, outbox):
    user = f.create_user(is_staff=True)
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

    f.create_usertype(slug='lead', display_name='Regional Lead')

    location1 = f.create_locaiton()
    user.profile.location = location1
    user.profile.save()

    url = base_url + '/region/'
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    browser.visit(url)
    lead_create_link = browser.find_by_text('Add Regional Lead')[0]
    assert lead_create_link
    lead_create_link.click()
    browser.select('location', location1.id)
    browser.select('leads', user.id)
    browser.find_by_css('[type=submit]')[0].click()
