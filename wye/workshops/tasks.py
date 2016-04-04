from celery import task
import datetime
from django.core.mail import EmailMessage
import os
from wye.workshops.models import Workshop


@task
def workshop_reminder():
    # date after one week to filter out workshops
    workshop_date = datetime.date.today() + datetime.timedelta(days=7)
    workshops = Workshop.objects.filter(expected_date=workshop_date)
    for workshop in workshops:
        if workshop.is_active:
            presenter_email = list()
            requester_email = list()

            # getting all requesters email
            requesters = workshop.requester.user.all()
            for requester in requesters:
                requester_email.append(requester.email)

            # getting all presenters email
            presenters = workshop.presenter.all()
            for presenter in presenters:
                presenter_email.append(presenter.email)

            recipents = presenter_email + requester_email
            # modify message according to need
            message = "Hi, you have workshop scheduled for {workshop_date}."
            email = EmailMessage("[Workshop] Gentle Reminder",
                                 message,
                                 os.environ.get('EMAIL_HOST_USER', ''),
                                 recipents)
            email.send()
