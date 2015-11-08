from django import template
from wye.base.constants import WorkshopStatus

register = template.Library()


def show_draft_button(workshop, user):
    if workshop.status in [WorkshopStatus.REQUESTED,
                           WorkshopStatus.ACCEPTED,
                           WorkshopStatus.DECLINED]:
        return True
    return False
register.filter(show_draft_button)


def show_requested_button(workshop, use):
    if workshop.status == WorkshopStatus.DRAFT:
        return True
    return False

register.filter(show_requested_button)


def show_accepted_button(workshop, use):
    if workshop.status == WorkshopStatus.REQUESTED:
        return True
    return False

register.filter(show_accepted_button)


def show_feedback_button(workshop, use):
    if workshop.status == WorkshopStatus.COMPLETED:
        return True
    return False

register.filter(show_feedback_button)


def show_decline_button(workshop, use):
    if workshop.status == WorkshopStatus.ACCEPTED:
        return True
    return False
register.filter(show_decline_button)
