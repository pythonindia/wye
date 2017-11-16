# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.core.urlresolvers import reverse, reverse_lazy
# from django.http import HttpResponseRedirect, JsonResponse
# from django.shortcuts import get_object_or_404
# from django.views import generic


import os
from io import BytesIO
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
import xlrd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.colors import black, red
# from wye.profiles.models import Profile
from wye.base.views import add_user_create_reset_password_link
# from wye.base.constants import WorkshopStatus
from wye.base.emailer_html import (
    send_email_to_id, send_email_to_id_with_attachment)
from .forms import WorkshopCertificateForm
from .utils import make_certi
from .models import Workshop

from wye.profiles.models import UserType


def send_email_certificate(request, pk):
    template_name = "workshops/students/email_certificate.html"
    context_dict = {}
    workshop = Workshop.objects.get(pk=pk)
    context_dict['workshop'] = workshop
    if request.method == 'POST':
        form = WorkshopCertificateForm(request.POST, request.FILES)
        context_dict['form'] = form
        if form.is_valid():
            f = request.FILES['file']
            Book = xlrd.open_workbook(file_contents=f.read())
            WorkSheet = Book.sheet_by_index(0)

            num_row = WorkSheet.nrows - 1
            row = 0
            error_list = []
            error_count = 0
            while row < num_row:
                row += 1
                first_name = WorkSheet.cell_value(row, 0)
                last_name = WorkSheet.cell_value(row, 1)
                email = WorkSheet.cell_value(row, 2)
                mobile = WorkSheet.cell_value(row, 3)
                workshop_name = workshop.workshop_section.name
                institute = workshop.requester.name
                workshop_date = workshop.expected_date
                filename = make_certi(
                    last_name, workshop_name,
                    institute, str(workshop_date))

                if filename != -1:
                    from wye.profiles.models import UserType
                    student_user_type = UserType.objects.get(slug='student')
                    user, newly_created = add_user_create_reset_password_link(
                        first_name, last_name, email, mobile,
                        student_user_type)
                    workshop.student_attended.add(user)
                    workshop.requester.students.add(user)
                    email_context = {
                        'workshop_section': workshop_name,
                        'workshop_date': workshop_date,
                        'full_name': '{} {}'.format(first_name, last_name)
                    }
                    subject = "[PythonExpress] Certificate of Participation"
                    text_body = loader.get_template(
                        'email_messages/workshop/students/certificate_created.txt').render(email_context)
                    email_body = loader.get_template(
                        'email_messages/workshop/students/certificate_created.html').render(email_context)
                    send_email_to_id_with_attachment(
                        subject,
                        body=email_body,
                        email_id=email,
                        text_body=text_body,
                        filename=filename)
                    os.remove(filename)

                else:
                    error_list.append('{} {}'.format(first_name, last_name))
                    error_count += 1
        return render(request, template_name, context_dict)
    form = WorkshopCertificateForm()
    context_dict['form'] = form
    return render(request, template_name, context_dict)


def register_students(request, pk):
    template_name = "workshops/students/register.html"
    context_dict = {}
    workshop = Workshop.objects.get(pk=pk)
    context_dict['workshop'] = workshop
    if request.method == 'POST':
        # form = WorkshopCertificateForm(request.POST, request.FILES)

        form = WorkshopCertificateForm(request.POST, request.FILES)
        context_dict['form'] = form
        if form.is_valid():
            f = request.FILES['file']
            Book = xlrd.open_workbook(file_contents=f.read())
            WorkSheet = Book.sheet_by_index(0)
            num_row = WorkSheet.nrows - 1
            row = 0
            while row < num_row:
                row += 1
                first_name = WorkSheet.cell_value(row, 0)
                last_name = WorkSheet.cell_value(row, 1)
                email = WorkSheet.cell_value(row, 2)
                mobile = WorkSheet.cell_value(row, 3)
                workshop_name = workshop.workshop_section.name
                institute = workshop.requester.name
                workshop_date = workshop.expected_date
                presenters = workshop.presenter.all()
                presenters_name = "\n".join(
                    ["{} {}".format(p.first_name, p.last_name) for p in presenters])
                student_user_type = UserType.objects.get(slug='student')
                user, newly_created = add_user_create_reset_password_link(
                    first_name, last_name, email, mobile, student_user_type)
                workshop.student_attended.add(user)
                workshop.requester.students.add(user)
                email_context = {
                    'workshop_section': workshop_name,
                    'workshop_date': workshop_date,
                    'full_name': '{} {}'.format(first_name, last_name)
                }
                subject = "[PythonExpress] Welcome "
                text_body = loader.get_template(
                    'email_messages/workshop/students/welcome.txt').render(email_context)
                email_body = loader.get_template(
                    'email_messages/workshop/students/welcome.html').render(email_context)
                send_email_to_id(
                    subject,
                    body=email_body,
                    email_id=email,
                    text_body=text_body)

        return render(request, template_name, context_dict)
    form = WorkshopCertificateForm()
    context_dict['form'] = form
    return render(request, template_name, context_dict)


def download_student_certificate(request, pk):

    # ------------------------------------------------------------
    workshop = Workshop.objects.get(pk=pk)
    first_name = request.user.first_name
    last_name = request.user.last_name
    workshop_name = workshop.workshop_section.name
    institute = workshop.requester.name
    workshop_date = workshop.expected_date
    presenters = workshop.presenter.all()
    presenters_name = "\n".join(
        ["{} {}".format(p.first_name, p.last_name) for p in presenters])
    name = '{} {}'.format(first_name, last_name)
    file_name = "python_express_certificate_{}.pdf".format(first_name)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(
        file_name)

    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Write content to certificate
    can.setFont("Courier-BoldOblique", 20)
    can.drawCentredString(3 * (1056 / 8), 360, 'This is to Certify that',)
    can.setFont("Helvetica-Bold", 30)
    can.setFillColor(red)
    can.drawCentredString(3 * (1056 / 8), 310, name,)
    can.setFillColor(black)
    can.setFont("Courier-BoldOblique", 20)
    can.drawCentredString(3 * (1056 / 8), 270,
                          'has successfully completed',)
    can.setFont("Helvetica-Bold", 25)
    can.drawCentredString(3 * (1056 / 8), 220, workshop_name,)
    can.setFont("Courier-BoldOblique", 20)
    can.drawCentredString(3 * (1056 / 8), 180,
                          'workshop held on ' + str(workshop_date),)

    can.drawCentredString(3 * (1056 / 8), 150, ' at ' + institute,)

    can.drawCentredString(3 * (1056 / 20), 100, presenters_name,)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # read your existing PDF
    existing_pdf = PdfFileReader(open("template_certificate.pdf", "rb"))
    output = PdfFileWriter()

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    output.write(response)
    return response
