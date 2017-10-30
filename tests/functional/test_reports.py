from .. import factories as f
from wye.base.constants import WorkshopStatus
from .. utils import create_user_verify_login


def test_report_home_page(base_url, browser, outbox):
    f.create_usertype(slug='tutor', display_name='tutor')
    user = create_user_verify_login(base_url, browser, outbox)
    location1 = f.create_locaiton()
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    user.profile.usertype.clear()
    user.profile.usertype.add(poc_type)
    user.profile.location = location1
    user.profile.save()
    user.save()

    org = f.create_organisation()
    org.user.add(user)
    user.profile.interested_locations.add(org.location)
    user.profile.location = org.location
    user.profile.save()
    org.save()

    workshop = f.create_workshop(requester=org)
    workshop.status = WorkshopStatus.COMPLETED
    workshop.save()

    url = base_url + '/reports/'
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    browser.visit(url)

    user.is_staff = True
    user.save()
    browser.visit(url)
    org_create_link = browser.find_by_text('Total workshops')[0]
    assert org_create_link


def test_report_page(base_url, browser, outbox):
    f.create_usertype(slug='tutor', display_name='tutor')
    user = create_user_verify_login(base_url, browser, outbox)
    user.is_staff = True
    user.save()

    location2 = f.create_locaiton()
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    user.profile.usertype.clear()
    user.profile.usertype.add(poc_type)
    user.profile.location = location2
    user.profile.save()
    user.save()
    org = f.create_organisation()
    org.user.add(user)
    section1 = f.create_workshop_section(name='section1')

    w1 = f.create_workshop(requester=org, workshop_section=section1)
    w1.presenter.add(user)
    w2 = f.create_workshop(requester=org, workshop_section=section1)
    w2.presenter.add(user)
    w3 = f.create_workshop(requester=org, workshop_section=section1)
    w3.presenter.add(user)
    w4 = f.create_workshop(requester=org, workshop_section=section1)
    w4.presenter.add(user)
    w5 = f.create_workshop(requester=org, workshop_section=section1)
    w5.presenter.add(user)

    url = base_url + '/reports/'
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()

    browser.visit(url)
    browser.find_by_css('[name=workshops]')[0].click()

    browser.visit(url)
    browser.select('years', 2016)
    browser.select('usertype', 'all')
    browser.find_by_css('[name=workshops]')[0].click()

    browser.visit(url)
    browser.select('years', 'all')
    browser.select('usertype', 'all')
    browser.find_by_css('[name=workshops]')[0].click()

    browser.visit(url)
    browser.select('years', 'all')
    browser.select('usertype', 'all')
    browser.find_by_css('[name=workshops]')[0].click()

    browser.visit(url)
    browser.select('years', 'all')
    browser.select('usertype', 'tutor')
    browser.find_by_css('[name=workshops]')[0].click()

    browser.visit(url)
    browser.select('years', 'all')
    browser.select('usertype', 'poc')
    browser.find_by_css('[name=workshops]')[0].click()

    browser.visit(url)
    browser.find_by_css('[name=users]')[0].click()
