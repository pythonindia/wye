import base
from tests import factories as f

outbox_len = 0
password = '123123'


def test_presenter_info(base_url, browser, outbox):
    '''
    Test the flow of getting presenter information from workshop page.
    '''

    f.create_usertype(slug='tutor', display_name='tutor')
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    state = f.create_state()

    user = base.create_user(password)

    url = base_url + '/workshop/'
    base.login_and_confirm(browser, url, outbox, user, password)
    user.save()
    location = f.create_locaiton(name='location1')
    user.profile.location = location
    user.profile.usertype.clear()
    user.profile.usertype.add(poc_type)
    user.profile.interested_states.add(state)
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
    org.save()
    section1 = f.create_workshop_section(name='section1')

    url = base_url + '/workshop/create/'
    base.workshop_create(browser, url, org, section1)

    # accept the workshop
    # accpet_btn = browser.find_by_css(".ws-accept")[0]
    accept_workshop_link = browser.find_by_text('Accept')[0]
    workshop_row = accept_workshop_link.find_by_xpath(".//ancestor::tr")[0]

    accept_workshop_link.click()
    workshop_row.click()
    assert browser.title, "Workshop Details"

    # find and click user's full name on the details page
    browser.find_by_text(user.get_full_name())[1].click()

    # veify that profile was indeed open
    assert browser.title, "My Profile"
    assert browser.title, user.get_full_name()
