from datetime import datetime, timedelta

import base
from tests import factories as f
from wye.base.constants import WorkshopStatus, WorkshopLevel
from wye.workshops.tasks import workshop_reminder, workshop_feedback

outbox_len = 0
password = '123123'


def test_workshop_celery_task(base_url, browser, outbox):
    """
    """

    # Create usertypes
    f.create_usertype(
        slug='lead', display_name='regional lead')
    f.create_usertype(slug='tutor', display_name='tutor')
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    state = f.create_state()
    # Testcase with usertyep poc
    user = base.create_user(password)
    url = base_url + '/login/'
    base.login_and_confirm(browser, url, outbox, user, password)
    user.profile.usertype.clear()
    user.profile.usertype.add(poc_type)
    user.profile.interested_states.add(state)
    user.profile.save()
    user.save()

    # Create org
    location = f.create_locaiton(state=state)
    org = f.create_organisation(location=location)
    org.user.add(user)
    user.profile.interested_locations.add(location)
    user.profile.location = org.location
    user.profile.save()
    org.save()

    # Create workshop
    workshop = f.create_workshop(requester=org)
    workshop.expected_date = datetime.now() + timedelta(days=1)
    workshop.status = WorkshopStatus.REQUESTED
    workshop.level = WorkshopLevel.BEGINNER
    workshop.location = org.location
    workshop.presenter.add(user)
    workshop.save()

    rst = workshop_reminder.apply(args=(1, 1)).get()
    assert rst

    rst = workshop_reminder.apply(args=(1, 0)).get()
    assert rst

    workshop.expected_date = datetime.now() + timedelta(days=2)
    workshop.save()
    rst = workshop_feedback.apply(args=(1,)).get()
    assert rst
