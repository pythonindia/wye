import os
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_mail(to, context, template_dir=None):
    """
    Utility to send mail.
    param to: recipient email list.
    param context: dict containing parameter, that will be passed
        to message templates.
    param template_dir: Path to directory, where required files for
        email exists. such as subject.txt, message.txt etc.
    """

    to_str = lambda x: render_to_string(os.path.join(template_dir, x),
                                        context).strip()
    subject = to_str('subject.txt')
    from_email = settings.DEFAULT_FROM_EMAIL
    text_message = to_str('message.txt')
    html_message = to_str('message.html')
    recipient_list = to

    return send_mail(subject, text_message, from_email,
                    to, html_message=None)

