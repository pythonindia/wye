from datetime import datetime, timedelta

import re
from wye.base.constants import WorkshopStatus
from .. import factories as f


def test_workshop_flow(base_url, browser, outbox):
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

    poc_type = f.create_usertype(slug='poc', display_name='poc')
    user.profile.usertype.add(poc_type)
    user.save()
    org = f.create_organisation()
    org.user.add(user)
    user.profile.interested_locations.add(org.location)
    org.save()

    workshop = f.create_workshop(requester=org)

    workshop.expected_date = datetime.now() + timedelta(days=20)
    # workshop.presenter.add(user)
    workshop.status = WorkshopStatus.REQUESTED
    workshop.location = org.location
    workshop.save()
    url = base_url + '/workshop/update/{}/'.format(workshop.id)
    browser.visit(url)
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    tutor_type = f.create_usertype(slug='tutor', display_name='tutor')
    user.profile.usertype.remove(poc_type)
    user.profile.usertype.add(tutor_type)
    user.save()

    url = base_url + '/workshop/'
    browser.visit(url)

    accept_workshop_link = browser.find_by_text('Accept')[0]
    assert accept_workshop_link
    accept_workshop_link.click()

    reject_workshop_link = browser.find_by_text('Reject')[0]
    assert reject_workshop_link
    reject_workshop_link.click()

    user.profile.usertype.remove(tutor_type)
    user.profile.usertype.add(poc_type)
    user.save()
    hold_workshop_link = browser.find_by_text('Hold')[0]
    assert hold_workshop_link
    hold_workshop_link.click()

    publish_workshop_link = browser.find_by_text('Publish/Request')[0]
    assert publish_workshop_link
    publish_workshop_link.click()

    workshop.expected_date = datetime.now() + timedelta(days=-20)
    workshop.save()
    f.create_workshop_rating()
#     publish_workshop_link = browser.find_by_text('Share Feedback')[0]
#     assert publish_workshop_link
#     publish_workshop_link.click()
    url = base_url + '/workshop/feedback/{}'.format(workshop.id)
    browser.visit(url)
    browser.check('rating0-1')
    browser.fill('comment', "Testing comments")

    browser.find_by_css('[type=submit]')[0].click()
