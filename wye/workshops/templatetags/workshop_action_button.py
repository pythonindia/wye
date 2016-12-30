from datetime import datetime

from django import template

from wye.base.constants import WorkshopStatus
from wye.profiles.models import Profile


register = template.Library()


def show_draft_button(workshop, user):
    if (workshop.status in [WorkshopStatus.REQUESTED,
                            WorkshopStatus.ACCEPTED,
                            WorkshopStatus.DECLINED] and
            user in workshop.requester.user.all()):
        return True
    return False

register.filter(show_draft_button)


def show_requested_button(workshop, user):
    if (workshop.status == WorkshopStatus.HOLD and
            user in workshop.requester.user.all()):

        return True
    return False

register.filter(show_requested_button)


def show_accepted_button(workshop, user):
    if (workshop.status == WorkshopStatus.REQUESTED):
        return True
    return False

register.filter(show_accepted_button)


def show_feedback_button(workshop, user):
    if ((workshop.status == WorkshopStatus.COMPLETED or
         datetime.now().date() > workshop.expected_date) and
        (user in workshop.requester.user.all() or
         user in workshop.presenter.all())):
        return True
    return False

register.filter(show_feedback_button)


def show_reject_button(workshop, user):
    if (workshop.status == WorkshopStatus.ACCEPTED and
            user in workshop.presenter.all()):

        return True
    return False

register.filter(show_reject_button)


def show_decline_button(workshop, user):
    neglected_workshops = [WorkshopStatus.COMPLETED,
                           WorkshopStatus.FEEDBACK_PENDING,
                           WorkshopStatus.DECLINED]
    if (workshop.status not in neglected_workshops and
            user in workshop.requester.user.all()):
        return True
    return False
register.filter(show_decline_button)



def show_volunteer_count(user):
    if not Profile.is_presenter(user):
        return True
    return False
register.filter(show_volunteer_count)


def show_accept_volunteer_button(workshop, user):
    if Profile.is_volunteer(user) and user not in workshop.volunteer.all() and  user not in workshop.requester.user.all():
        return True
    return False
register.filter(show_accept_volunteer_button)


def show_opt_out_volunteer_button(workshop, user):
    if user in workshop.volunteer.all():
        return True
    return False
register.filter(show_opt_out_volunteer_button)
