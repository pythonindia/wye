from tests import base
from tests import factories as f

outbox_len = 0
password = '123123'


def test_workshop_create(base_url, browser, outbox):
    """
    """
    f.create_usertype(slug='tutor', display_name='tutor')
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    state = f.create_state()
    user = base.create_user(password)
    url = base_url + '/workshop/'
    base.login_and_confirm(browser, url, outbox, user, password)
    user.save()
    location = f.create_locaiton(name='location1')
    section1 = f.create_workshop_section(name='section1')

    user.profile.location = location
    user.profile.usertype.clear()
    user.profile.usertype.add(poc_type)
    user.profile.interested_states.add(state)
    user.profile.mobile = '1234567890'
    # browser.select('usertype', poc_type.id)
    user.profile.interested_sections.add(section1)
    user.profile.occupation = 'occupation'
    user.profile.work_location = 'work_location'

    user.profile.save()

    url = base_url + '/workshop/'
    base.login(browser, url, user, password)

    # validate if user belongs to organisation
    url = base_url + '/workshop/create/'
    browser.visit(url)
    assert browser.is_text_present("create organisaiton.")
    # Create org
    org = f.create_organisation(location=location)
    org.user.add(user)
    user.profile.interested_locations.add(org.location)
#     user.profile.location = org.location
#     user.profile.save()
    org.save()
    # section1 = f.create_workshop_section(name='section1')

    # invalid form
    url = base_url + '/workshop/create/'
    browser.visit(url)
    browser.select('no_of_participants', 10)
    browser.fill('expected_date', '11/12/2018')
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')
    # valid form
    url = base_url + '/workshop/create/'
    base.workshop_create(browser, url, org, section1)
