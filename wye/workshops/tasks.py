import datetime
import os
from celery import task

from django.template import Context, loader
# from django.template.loader import get_template

from wye.workshops.models import Workshop
from wye.base.emailer_html import send_email_to_id


EMAIL_HOST = os.environ.get('EMAIL_HOST_USER', '')


def intro_emails(organisation, email_context, email_id):
    subject = '[PythonExpress] Intro for workshop at {}, {}'.format(
        organisation.name, organisation.location.name)
    email_body = loader.get_template(
        'email_messages/workshop/workshop_intro_email.html').render(
        email_context)
    text_body = loader.get_template(
        'email_messages/workshop/workshop_intro_email.txt').render(
        email_context)
    send_email_to_id(
        subject,
        body=email_body,
        email_id=email_id,
        text_body=text_body)


def remainder_email(organisation, email_context, email_id):
    subject = '[PythonExpress] Remainder for workshop at {}, {}'.format(
        organisation.name, organisation.location.name)
    email_body = loader.get_template(
        'email_messages/workshop/remainder.html').render(email_context)
    text_body = loader.get_template(
        'email_messages/workshop/remainder.txt').render(email_context)
    send_email_to_id(
        subject,
        body=email_body,
        email_id=email_id,
        text_body=text_body)


def feedback_emails(organisation, email_context, email_id):
    subject = '[PythonExpress] Request for Workshop Feedback {}, {}'.format(
        organisation.name, organisation.location.name)
    email_body = loader.get_template(
        'email_messages/workshop/feedback_email.html').render(
        email_context)
    text_body = loader.get_template(
        'email_messages/workshop/feedback_email.txt').render(
        email_context)
    send_email_to_id(
        subject,
        body=email_body,
        email_id=email_id,
        text_body=text_body)


@task
def workshop_reminder(days, intro=None, feedback=None):
    """
    send workshop reminder and intro email to all register user
    :return:
    """
    if feedback:
        today = datetime.datetime.today()
        if days:
            workshop_date = today + datetime.timedelta(days=2)
            workshops = Workshop.objects.filter(expected_date=workshop_date)

            for workshop in workshops:
                context_dict = {
                    'date': workshop_date,
                    'workshop_title': workshop.workshop_section.name,
                }
                email_context = Context(context_dict)
                organisation = workshop.requester
                for requester in workshop.requester.user.all():
                    feedback_emails(
                        organisation, email_context, requester.email)
                for presenter in workshop.presenter.all():
                    feedback_emails(
                        organisation, email_context, presenter.email)
    else:
        workshop_date = datetime.date.today() + datetime.timedelta(days=days)
        workshops = Workshop.objects.select_related(
            'workshop_section').filter(
            expected_date=workshop_date).filter(
            is_active=True)

        for workshop in workshops:
            organisation = workshop.requester

            context_dict = {
                'date': workshop_date,
                'workshop_title': workshop.workshop_section.name,
            }
            if workshop.get_presenter_list:
                context_dict['poc_list'] = workshop.requester.user.all()
                context_dict['presenter_list'] = workshop.presenter.all()

                if intro:

                    # Below  loop is to send email individually
                    email_context = Context(context_dict)
                    for requester in workshop.requester.user.all():
                            intro_emails(
                                organisation, email_context, requester.email)
                    for presenter in workshop.presenter.all():
                            intro_emails(
                                organisation, email_context, presenter.email)
                else:
                    context_dict['workshop_title'] = workshop.workshop_section.name
                    context_dict['workshop_date'] = workshop.expected_date
                    context_dict['trainer'] = workshop.presenter.all()
                    context_dict['venue'] = """{} , {}""".format(
                        workshop.requester.name,
                        workshop.requester.full_address)
                    context_dict['organiser'] = workshop.requester.name
                    email_context = Context(context_dict)
                    for requester in workshop.requester.user.all():
                        remainder_email(
                            organisation, email_context, requester.email)
                    for presenter in workshop.presenter.all():
                        remainder_email(
                            organisation, email_context, presenter.email)
    return True


# @task
# def workshop_feedback(days=None):
#     today = datetime.datetime.today()
#     if days:
#         workshop_date = today + datetime.timedelta(days=2)
#     workshops = Workshop.objects.filter(expected_date=workshop_date)

#     for workshop in workshops:
#         context_dict = {
#             'date': workshop_date,
#             'workshop_title': workshop.workshop_section.name,
#         }
#         email_context = Context(context_dict)
#         organisation = workshop.requester
#         for requester in workshop.requester.user.all():
#             feedback_emails(organisation, email_context, requester.email)
#         for presenter in workshop.presenter.all():
#             feedback_emails(organisation, email_context, presenter.email)

#     return True


# def get_workshop_recipients(workshop):
#     """
#     Filter out all recipients including requesters as well as presenters
#     :param workshop: workshop object
#     :return: list of all recipients w.r.t workshop
#     """

#     presenter_email = list()
#     requester_email = list()

#     requesters = workshop.requester.user.all()
#     for requester in requesters:
#         requester_email.append(requester.email)

#     presenters = workshop.presenter.all()
#     for presenter in presenters:
#         presenter_email.append(presenter.email)

#     recipients = presenter_email + requester_email

#     return recipients
