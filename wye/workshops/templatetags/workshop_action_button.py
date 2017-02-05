from datetime import datetime

from django import template
from wye.base.constants import WorkshopStatus, FeedbackType
from wye.profiles.models import Profile

register = template.Library()


def show_feedback_button(workshop, user):
    if (workshop.status == WorkshopStatus.COMPLETED or
            datetime.now().date() > workshop.expected_date):
        if (workshop.is_presenter(user) and
            workshop.workshopfeedback_set.filter(
                feedback_type=FeedbackType.PRESENTER).count() <= 0 or
            (workshop.is_organiser(user) and
                workshop.workshopfeedback_set.filter(
                feedback_type=FeedbackType.ORGANISATION).count() <= 0)):
            return True
        else:
            return False
    return False


def show_draft_button(workshop, user):
    if (workshop.status in [WorkshopStatus.REQUESTED,
                            WorkshopStatus.ACCEPTED,
                            WorkshopStatus.DECLINED] and
            user in workshop.requester.user.all() and
            not show_feedback_button(workshop, user)):
        return True
    return False


def show_requested_button(workshop, user):
    if (workshop.status == WorkshopStatus.HOLD and
            user in workshop.requester.user.all() and
            not show_feedback_button(workshop, user)):

        return True
    return False


def show_accepted_button(workshop, user):
    if (workshop.status == WorkshopStatus.REQUESTED):
        return True
    return False


def show_reject_button(workshop, user):
    if (workshop.status == WorkshopStatus.ACCEPTED and
            user in workshop.presenter.all() and
            not show_feedback_button(workshop, user)):

        return True
    return False


def show_decline_button(workshop, user):
    neglected_workshops = [WorkshopStatus.COMPLETED,
                           WorkshopStatus.FEEDBACK_PENDING,
                           WorkshopStatus.DECLINED]
    if (workshop.status not in neglected_workshops and
            user in workshop.requester.user.all() and
            not show_feedback_button(workshop, user)):
        return True
    return False


def show_volunteer_count(user):
    if workshop.status >= WorkshopStatus.ACCEPTED:
        return True
    return False


def show_accept_volunteer_button(workshop, user):
    number_of_volunteers = 0 if not workshop.number_of_volunteers else workshop.number_of_volunteers
    if Profile.is_volunteer(user) and \
            number_of_volunteers - workshop.volunteer.count() >= 1 and \
            user not in workshop.volunteer.all() and  \
            user not in workshop.requester.user.all():
        return True
    return False


def show_opt_out_volunteer_button(workshop, user):
    if user in workshop.volunteer.all():
        return True
    return False


register.filter(show_accepted_button)
register.filter(show_requested_button)
register.filter(show_draft_button)
register.filter(show_reject_button)
register.filter(show_decline_button)
register.filter(show_volunteer_count)
register.filter(show_accept_volunteer_button)
register.filter(show_feedback_button)
register.filter(show_opt_out_volunteer_button)
