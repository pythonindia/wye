import re
from .. import factories as f


def test_regional_lead_flow(base_url, browser, outbox):
    tutor = f.create_usertype(slug='tutor', display_name='tutor')
    section1 = f.create_workshop_section()
    state = f.create_state()
    location = f.create_locaiton()
    user = f.create_user(is_staff=True)
    user.set_password('123123')
    user.profile.interested_locations.add(location)
    user.profile.location = location
    user.profile.interested_states.add(state)
    user.profile.mobile = '1234567890'
    user.profile.interested_sections.add(section1)
    user.profile.interested_level = 1
    user.profile.github = 'https://github.com'
    user.profile.save()
    user.save()

    user.save()

    user2 = f.create_user()
    user2.set_password('123123')
    user2.profile.interested_locations.add(location)
    user2.profile.location = location
    user2.profile.interested_states.add(state)
    user2.profile.mobile = '1234567890'
    user2.profile.interested_sections.add(section1)
    user2.profile.interested_level = 1
    user2.profile.github = 'https://github.com'
    user2.profile.save()
    user2.save()


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
    location2 = f.create_locaiton()
    user.profile.location = location1
    user.profile.save()
    user2.profile.location = location1
    user2.profile.save()

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

    regional_lead = f.create_regional_lead()
    regional_lead.location = location1
    regional_lead.leads = [user.id]
    regional_lead.save()

    url = base_url + '/region/lead/{}/edit/'.format(regional_lead.id)
    browser.visit(url)
    browser.select('location', location2.id)
    browser.select('location', location1.id)
    browser.select('leads', user2.id)
    browser.find_by_css('[value=Update]')[0].click()
