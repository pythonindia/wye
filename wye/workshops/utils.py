from django.template import loader
import os
import PyPDF2
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import black, red
from wye.profiles.models import Profile
from wye.base.emailer_html import send_email_to_id


def send_mail_to_group(context, workshop, exclude_emails=None):
    """
    Send email to org/group users.
    @param context: Is dict of data required by email template.
    @exclude_emails: Is list of email to be excluded from
    email update.
    """
    if exclude_emails is None:
        exclude_emails = []

    # Collage POC and admin email
    poc_admin_user = Profile.get_user_with_type(
        user_type=['admin']
    ).values_list('email', flat=True)
    # Org user email
    org_user_emails = workshop.requester.user.filter(
        is_active=True
    ).values_list('email', flat=True)
    # all presenter if any
    all_presenter_email = workshop.presenter.values_list(
        'email', flat=True
    )
    # List of tutor who have shown interest in that location
    region_interested_member = Profile.objects.filter(
        interested_states=workshop.requester.location.state,
        usertype__slug='tutor',
        enable_notifications=True
    ).values_list('user__email', flat=True)

    all_email = []
    all_email.extend(org_user_emails)
    all_email.extend(all_presenter_email)
    all_email.extend(poc_admin_user)
    all_email.extend(region_interested_member)
    all_email = set(all_email)
    all_email = list(all_email.difference(exclude_emails))

    subject = '[PythonExpress] Workshop request status.'
    email_body = loader.get_template(
        'email_messages/workshop/create_workshop/message.html').render(
        context)
    text_body = loader.get_template(
        'email_messages/workshop/create_workshop/message.txt').render(
        context)
    for email_id in all_email:
        send_email_to_id(
            subject,
            body=email_body,
            users_list=email_id,
            text_body=text_body)


def make_certi(name, workshop_name, institute, workshop_date):
    outputfiletemp = 'testoutput.pdf'
    pdf1File = open('template_certificate.pdf', 'rb')
    pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
    pdfWriter = PyPDF2.PdfFileWriter()

    packet = BytesIO()
    cv = canvas.Canvas(packet, pagesize=letter)
    cv.setPageSize(landscape(letter))
    # create a string
    cv.setFont("Courier-BoldOblique", 20)
    cv.drawCentredString(3 * (1056 / 8), 360, 'This is to Certify that',)
    cv.setFont("Helvetica-Bold", 30)
    cv.setFillColor(red)
    cv.drawCentredString(3 * (1056 / 8), 310, name,)
    cv.setFillColor(black)
    cv.setFont("Courier-BoldOblique", 20)
    cv.drawCentredString(3 * (1056 / 8), 270,
                         'has successfully completed',)
    cv.setFont("Helvetica-Bold", 25)
    cv.drawCentredString(3 * (1056 / 8), 220, workshop_name,)
    cv.setFont("Courier-BoldOblique", 20)
    cv.drawCentredString(3 * (1056 / 8), 180,
                         'workshop held on ' + str(workshop_date),)

    cv.drawCentredString(3 * (1056 / 8), 150, ' at ' + institute,)
    cv.save()
    # write to a file
    with open(outputfiletemp, 'wb') as fp:
        fp.write(packet.getvalue())

    certFirstPage = pdf1Reader.getPage(0)
    # o = open(outputfiletemp, 'rb')
    pdfWatermarkReader = PyPDF2.PdfFileReader(outputfiletemp)
    certFirstPage.mergePage(pdfWatermarkReader.getPage(0))
    pdfWriter.addPage(certFirstPage)

    pdfOutputFile = open('certificate_' + name + '.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)
    pdfOutputFile.close()
    pdf1File.close()
    os.remove('testoutput.pdf')
    return 'certificate_' + name + '.pdf'
