from django import template
from datetime import datetime
from wye.base.constants import WorkshopStatus
register = template.Library()


def show_draft_button(workshop, user):
    if workshop.status in [WorkshopStatus.REQUESTED,
                           WorkshopStatus.ACCEPTED,
                           WorkshopStatus.DECLINED]:

        requester_members = workshop.requester.user.values()

        for member in requester_members:
            if user.username == member['username']:
                return True

    return False
register.filter(show_draft_button)


def show_requested_button(workshop, user):
    if workshop.status == WorkshopStatus.HOLD:

        requester_members = workshop.requester.user.values()

        for member in requester_members:
            if user.username == member['username']:
                return True

    return False

register.filter(show_requested_button)


def show_accepted_button(workshop, user):
    if workshop.status == WorkshopStatus.REQUESTED:
        return True
    return False

register.filter(show_accepted_button)


def show_feedback_button(workshop, user):

    is_requester = False
    is_presenter = False
    is_completed = False

    if workshop.status == WorkshopStatus.COMPLETED:

        requester_members = workshop.requester.user.values()
        presenters = workshop.presenter.values()

        for member in requester_members:
            if user.username == member['username']:
                is_requester = True

        for presenter in presenters:
            if user.username == presenter['username']:
                is_presenter = True

        if datetime.now().date() > workshop.expected_date:
            is_completed = True

        if is_completed and (is_requester or is_presenter):
            return True

    return False

register.filter(show_feedback_button)


def show_decline_button(workshop, user):
    if workshop.status == WorkshopStatus.ACCEPTED:

        presenters = workshop.presenter.values()

        for presenter in presenters:
            if user.username == presenter['username']:
                return True

    return False

register.filter(show_decline_button)
