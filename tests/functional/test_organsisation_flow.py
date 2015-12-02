import re
from .. import factories as f


def test_organisation_flow(base_url, browser, outbox):
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

    poc_type = f.create_usertype(slug='poc', display_name='poc')
    user.profile.usertype.add(poc_type)
    user.save()
    location1 = f.create_locaiton(name='location1')
    location2 = f.create_locaiton(name='location2')

    url = base_url + '/organisation/'
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    browser.visit(url)
    org_create_link = browser.find_by_text('Add Organisation')[0]
    assert org_create_link
    org_create_link.click()
    browser.select('organisation_type', 1)
    browser.fill('name', 'Org1')
    browser.fill('description', 'Description')
    browser.select('location', 1)
    browser.fill('organisation_role', 'Role1')
    browser.find_by_css('[type=submit]')[0].click()
    # browser.find_by_css('[clickable-row]')[0].click()
    browser.find_by_text('Org1')[0].click()
    browser.find_by_text('Edit')[0].click()
    browser.fill('organisation_role', 'Role updated')
    browser.find_by_css('[type=submit]')[0].click()
    browser.find_by_text('Org1')[0].click()
    browser.find_by_text('Delete')[0].click()