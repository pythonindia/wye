from django import template
from datetime import datetime
from wye.base.constants import WorkshopStatus
register = template.Library()


def show_draft_button(workshop, user):
    if (workshop.status in [WorkshopStatus.REQUESTED,
                            WorkshopStatus.ACCEPTED,
                            WorkshopStatus.DECLINED]
            and user in workshop.requester.user.all()):
        return True
    return False

register.filter(show_draft_button)


def show_requested_button(workshop, user):
    if (workshop.status == WorkshopStatus.HOLD
            and user in workshop.requester.user.all()):

        return True
    return False

register.filter(show_requested_button)


def show_accepted_button(workshop, user):
    if workshop.status == WorkshopStatus.REQUESTED:
        return True
    return False

register.filter(show_accepted_button)


def show_feedback_button(workshop, user):
    if (workshop.status == WorkshopStatus.COMPLETED
            and (user in workshop.requester.user.all()
                 or user in workshop.presenter.all())
            and datetime.now().date() > workshop.expected_date):

        return True
    return False

register.filter(show_feedback_button)


def show_decline_button(workshop, user):
    if (workshop.status == WorkshopStatus.ACCEPTED
            and user in workshop.presenter.all()):

        return True
    return False

register.filter(show_decline_button)
