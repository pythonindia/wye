from tests import base
from datetime import datetime, timedelta
from tests import factories as f
from .. utils import create_user_verify_login
from wye.base.constants import WorkshopStatus

# import os
outbox_len = 0
password = '123123'


def test_student_profile_create(base_url, browser, outbox):
    """
    """
    student_poc = f.create_usertype(slug='student', display_name='Student')
    f.create_usertype(slug='tutor', display_name='tutor')
    user = create_user_verify_login(base_url, browser, outbox)
    user.first_name = 'First Name'
    user.last_name = 'Last Name'
    user.save()
    location1 = f.create_locaiton()
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    user.profile.usertype.clear()
    user.profile.usertype.add(poc_type)
    user.profile.usertype.add(student_poc)
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
    workshop.expected_date = datetime.now() + timedelta(days=-20)
    workshop.status = WorkshopStatus.COMPLETED
    workshop.location = org.location
    workshop.student_attended.add(user)
    workshop.presenter.add(user)
    workshop.save()
    url = base_url + '/accounts/login/'
    base.login(browser, url, user, '123123')
    url = base_url + '/profile/' + user.username
    browser.visit(url)
    assert browser.is_text_present('Workshop Attended')
    download_link = browser.find_by_text('Download')[0]
    assert download_link
    download_link.click()
    download_url = base_url + \
        '/workshop/certificate/{}/download/'.format(workshop.id)
    browser.visit(download_url)


# def test_student_register(base_url, browser, outbox):
#     """
#     """
#     f.create_usertype(slug='student', display_name='Student')
#     f.create_usertype(slug='tutor', display_name='tutor')
#     user = create_user_verify_login(base_url, browser, outbox)
#     user.first_name = 'First Name'
#     user.last_name = 'Last Name'
#     user.save()
#     location1 = f.create_locaiton()
#     poc_type = f.create_usertype(slug='poc', display_name='poc')
#     user.profile.usertype.clear()
#     user.profile.usertype.add(poc_type)
#     user.profile.location = location1
#     user.profile.save()
#     user.save()

#     org = f.create_organisation()
#     org.user.add(user)
#     user.profile.interested_locations.add(org.location)
#     user.profile.location = org.location
#     user.profile.save()
#     org.save()

#     workshop = f.create_workshop(requester=org)
#     workshop.expected_date = datetime.now() + timedelta(days=-20)
#     workshop.status = WorkshopStatus.COMPLETED
#     workshop.location = org.location
#     workshop.student_attended.add(user)
#     workshop.presenter.add(user)
#     workshop.save()
#     url = base_url + '/accounts/login/'
#     base.login(browser, url, user, '123123')
#     url = base_url + '/workshop/student_register/{}/'.format(workshop.id)
#     browser.visit(url)

#     DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     print(DIR)
#     file_name = os.path.join(DIR, 'functional/student_list_format.xlsx')
#     print(file_name)
#     browser.attach_file(
#         'file', file_name)
#     browser.find_by_css('[type=submit]')[0].click()


# def test_student_email_certificate(base_url, browser, outbox):
#     """
#     """
#     f.create_usertype(slug='student', display_name='Student')
#     f.create_usertype(slug='tutor', display_name='tutor')
#     user = create_user_verify_login(base_url, browser, outbox)
#     user.first_name = 'First Name'
#     user.last_name = 'Last Name'
#     user.save()
#     location1 = f.create_locaiton()
#     poc_type = f.create_usertype(slug='poc', display_name='poc')
#     user.profile.usertype.clear()
#     user.profile.usertype.add(poc_type)
#     user.profile.location = location1
#     user.profile.save()
#     user.save()

#     org = f.create_organisation()
#     org.user.add(user)
#     user.profile.interested_locations.add(org.location)
#     user.profile.location = org.location
#     user.profile.save()
#     org.save()

#     workshop = f.create_workshop(requester=org)
#     workshop.expected_date = datetime.now() + timedelta(days=-20)
#     workshop.status = WorkshopStatus.COMPLETED
#     workshop.location = org.location
#     workshop.student_attended.add(user)
#     workshop.presenter.add(user)
#     workshop.save()
#     url = base_url + '/accounts/login/'
#     base.login(browser, url, user, '123123')
#     url = base_url + '/workshop/email_cetrificate/{}/'.format(workshop.id)
#     browser.visit(url)

#     # browser.find_by_css('input[type="file"]').first.click()
#     DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     file_name = os.path.join(DIR, 'functional/student_list_format.xlsx')
#     browser.attach_file(
#         'file', file_name)
#     browser.find_by_css('[type=submit]')[0].click()
