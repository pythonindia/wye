from celery import task
import datetime
import os

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

from wye.workshops.models import Workshop


EMAIL_HOST = os.environ.get('EMAIL_HOST_USER', '')


@task
def workshop_reminder(days, intro):
    """
    send workshop reminder and intro email to all register user
    :return:
    """
    template = get_template(
        'email_messages/workshop/workshop_intro_email.html')
    content = None
    workshop_date = datetime.date.today() + datetime.timedelta(days=days)
    workshops = Workshop.objects.select_related(
        'workshop_section').filter(expected_date=workshop_date)

    for workshop in workshops:
        if workshop.is_active:
            recipients = get_workshop_recipients(workshop)
            presenters = workshop.presenter.all()
            requesters = workshop.requester.user.all()
            for r in requesters:
                name = '{} {}'.format(r.first_name, r.last_name)
                poc_phone = '{}'.format(r.profile.mobile)
                poc_email = '{}'.format(r.email)
            "\n".join('{}, {} ,{}' .format(r.first_name, for r in requesters)
            if intro:
                context_dict = {
                    'date': workshop_date,
                    'workshop_title': workshop.workshop_section.name,
                    'poc_name': '',
                    'poc_email': '',
                    'poc_phone': '',
                    'trainer_name': '',
                    'trainer_email': '',
                    'trainer_phone': ''
                }
                context = Context(context_dict)
                content = template.render(context)

            for recipient in recipients:
                # Reminder Email
                message = "Hi, you have workshop scheduled for {workshop_date}.".format(
                    workshop_date)
                reminder_email = EmailMessage("[Workshop] Gentle Reminder",
                                              message,
                                              EMAIL_HOST,
                                              [recipient])
                reminder_email.send()

                # Intro Email
                if intro:
                    subject = 'Intro for workshop at {organisation_name}, {organisation_location}'
                    intro_email = EmailMultiAlternatives(subject,
                                                         from_email=EMAIL_HOST,
                                                         to=[recipient],
                                                         cc=['contact@pythonexpress.in '])
                    intro_email.attach_alternative(content, 'text/html')
                    intro_email.send()


@task
def workshop_feedback(days=None):
    today = datetime.datetime.today()
    if days:
        workshop_date = today - datetime.timedelta(days=2)
    workshops = Workshop.objects.filter(expected_date=workshop_date)

    template = get_template('email_messages/workshop/feedback_email.html')
    for workshop in workshops:
        if workshop.is_active:
            recipients = get_workshop_recipients(workshop)

            context = Context({'sender': 'pythonexpress.in '})
            content = template.render(context)
            for recipient in recipients:
                subject = 'Python Express Workshop Feedback {organiser} {venue}'
                feedback_email = EmailMultiAlternatives(subject,
                                                        from_email=EMAIL_HOST,
                                                        to=[recipient],
                                                        cc=['contact@pythonexpress.in '])
                feedback_email.attach_alternative(content, 'text/html')
                feedback_email.send()


def get_workshop_recipients(workshop):
    """
    Filter out all recipients including requesters as well as presenters
    :param workshop: workshop object
    :return: list of all recipients w.r.t workshop
    """

    presenter_email = list()
    requester_email = list()

    requesters = workshop.requester.user.all()
    for requester in requesters:
        requester_email.append(requester.email)

    presenters = workshop.presenter.all()
    for presenter in presenters:
        presenter_email.append(presenter.email)

    recipients = presenter_email + requester_email

    return recipients
