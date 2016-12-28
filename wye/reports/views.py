import datetime
import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from wye.base.constants import WorkshopStatus
from wye.workshops.models import Workshop
from wye.profiles.models import Profile


@login_required
def index(request):
    context_dict = {}
    if not request.user.is_staff:
        template_name = '403.html'
        return render(request, template_name, context_dict)

    workshops = Workshop.objects.filter(is_active=True)
    context_dict['workshops'] = {
        'completed': workshops.filter(status=WorkshopStatus.COMPLETED).count(),
        'drafted': workshops.filter(status=WorkshopStatus.DRAFT).count(),
        'hold': workshops.filter(status=WorkshopStatus.HOLD).count(),
        'feedback_pending': workshops.filter(
            status=WorkshopStatus.FEEDBACK_PENDING).count(),
    }
    workshop_finished = workshops.filter(
        status__in=[WorkshopStatus.COMPLETED,
                    WorkshopStatus.FEEDBACK_PENDING])
    tutors_dict = {}
    tutors = [
        user for w in workshop_finished for user in w.presenter.all()]
    for tutor in tutors:
        tutors_dict[tutor.id] = [
            tutor.username,
            tutor.first_name,
            tutor.last_name,
            tutor.profile.get_workshop_completed_count]
    context_dict['tutors'] = tutors_dict
    org_dict = {}
    orgs = [
        w.requester for w in workshop_finished]
    for org in orgs:
        if org.id in org_dict:
            count = org_dict[org.id][1] + 1
        else:
            count = 1
        org_dict[org.id] = [org.name, count, org.location.name]

    context_dict['orgs'] = org_dict
    template_name = 'reports/index.html'
    years = [('all', 'All')]
    for y in range(2016, int(datetime.datetime.today().strftime('%Y')) + 1):
        years.append((y, y))
    context_dict['years'] = years
    return render(request, template_name, context_dict)


@login_required
def get_tutor_college_poc_csv(request):
    if not request.user.is_staff:
        template_name = '403.html'
        return render(request, template_name, {})
    usertype = request.POST['usertype']
    year = request.POST['years']
    workshops = Workshop.objects.filter(is_active=True)
    if year != 'all':
        workshops = workshops.filter(expected_date__year=year)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="workshops.csv"'
    writer = csv.writer(response)
    csv_titles = ['Worshop Id', 'Workshop Date', 'Location', 'College']
    if usertype == 'tutor':
        csv_titles.extend(['Presenter Name', 'Presenter Email'])
    elif usertype == 'poc':
        csv_titles.extend(['College POC Name', 'College POC Email'])
    else:
        csv_titles.extend(['Presenter Name', 'Presenter Email'])
        csv_titles.extend(['College POC Name', 'College POC Email'])
    writer.writerow(csv_titles)

    for obj in workshops:
        row = [
            obj.id, obj.expected_date,
            obj.location.name, obj.requester.name]
        if usertype == 'tutor':
            for u in obj.presenter.all():
                row.append("{} {}".format(u.first_name, u.last_name))
                row.append("{}".format(u.email))
        elif usertype == 'poc':
            for u in obj.requester.user.all():
                row.append("{} {}".format(u.first_name, u.last_name))
                row.append("{}".format(u.email))
        else:
            for u in obj.presenter.all():
                row.append("{} {}".format(u.first_name, u.last_name))
                row.append("{}".format(u.email))
            for u in obj.requester.user.all():
                row.append("{} {}".format(u.first_name, u.last_name))
                row.append("{}".format(u.email))
        writer.writerow(row)
    return response


@login_required
def get_all_user_info(request):
    if not request.user.is_staff:
        template_name = '403.html'
        return render(request, template_name, {})
    users = User.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_users.csv"'
    writer = csv.writer(response)
    csv_titles = [
        'User Id', 'First Name', 'Last Name', 'Email', 'Is Active',
        'Is Presenter', 'Is POC', 'Is Regional Lead', 'Is Organiser']
    writer.writerow(csv_titles)
    for obj in users:
        row = [
            obj.id, obj.first_name, obj.last_name, obj.email, obj.is_active,
            Profile.is_presenter(obj),
            Profile.is_coordinator(obj),
            Profile.is_regional_lead(obj),
            Profile.is_organiser(obj)]

        writer.writerow(row)
    return response
