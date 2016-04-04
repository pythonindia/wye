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
            # getting all presenters email
            presenters = workshop.presenter.all()
            for presenter in presenters:
                presenter_email.append(presenter.email)

            # modify message according to need
            message = "Hi, you have workshop scheduled for {workshop_date}."
            email = EmailMessage("[Workshop] Gentle Reminder",
                                 message,
                                 os.environ.get('EMAIL_HOST_USER', ''),
                                 presenter_email)
            email.send()
