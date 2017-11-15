import datetime
import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django_pandas.io import read_frame, pd
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
    dataframe = read_frame(workshops, fieldnames=[
        'requester__location__state__name',
        'presenter__id',
        'presenter__first_name',
        'presenter__last_name',
        'workshop_level',
        'no_of_participants',
        'expected_date'])

    # State Based workshop plot
    location = dataframe
    location.dropna(subset=['presenter__id'], inplace=True)
    # location['presenter__id'] = location['presenter__id'].astype(int)
    location_based_sum = location.requester__location__state__name.value_counts()
    location_list = []
    for loc, count in location_based_sum.to_dict().items():
        location_list.append(
            {"label": loc, "values": count})
    context_dict['location'] = location_list
    # Top 10 tutors
    top_tutor_data = dataframe
    presenter_count = top_tutor_data.groupby('presenter__id').count()
    top_tutor_data.drop_duplicates(subset=['presenter__id'], inplace=True)
    top_tutor_data.index = top_tutor_data.presenter__id
    top_tutor_data.drop(["presenter__id"], axis=1, inplace=True)
    presenter_count.drop([
        'presenter__last_name', 'workshop_level',
        'requester__location__state__name',
        'no_of_participants',
        'expected_date'], axis=1, inplace=True)
    presenter_count.rename(columns={
        'presenter__first_name': 'conducted_workshop_count'}, inplace=True)
    t = top_tutor_data.join(presenter_count)
    top_ten_tutors = t.groupby('workshop_level')[
        'conducted_workshop_count'].nlargest(10)
    top_ten_tutors = dataframe.join(top_ten_tutors)
    top_ten_tutors.rename(
        columns={'presenter__first_name': 'first_name',
                 'presenter__last_name': 'last_name'
                 }, inplace=True)
    # Create list of dict as required by nd3 library
    d = {}
    data = []
    for index, row in top_ten_tutors.iterrows():
        d.setdefault(row.workshop_level, [])
        d[row.workshop_level].append(
            {'x': '{} {}'.format(row.first_name, row.last_name),
             'y': row.conducted_workshop_count})
    for k, v in d.items():
        data.append({'key': k, 'values': v})
    context_dict['workshop_tutor'] = data

    time_series = read_frame(workshops, fieldnames=[
        'no_of_participants', 'expected_date'])
    # print(time_series)
    time_series['no_of_participants'] = pd.to_numeric(
        time_series['no_of_participants'])
    time_series = time_series.groupby(
        'expected_date')[['no_of_participants']].agg('sum')
    time_series.fillna(0, inplace=True)
    time_series.index = pd.to_datetime(time_series.index)
    resampled = time_series.resample('M').sum()
    resampled.fillna(0, inplace=True)
    # month_list = []
    t = resampled.groupby([(resampled.index.year),
                           (resampled.index.month)]).sum()
    d = {}
    month_dict = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    for index, row in t.to_dict()['no_of_participants'].items():
        d.setdefault(index[0], [])
        d[index[0]].insert(
            index[1] - 1, {'x': month_dict.get(index[1]), 'y': row})

    ret = []
    for index, row in d.items():
        ret.append({"key": index, "values": row})
    print(ret)
    context_dict['line_graph'] = ret
    template_name = 'reports/index.html'
    return render(request, template_name, context_dict)


@login_required
def index_old(request):
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
    # if not request.user.is_staff:
    #     template_name = '403.html'
    #     return render(request, template_name, {})
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
    users = User.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_users.csv"'
    writer = csv.writer(response)
    csv_titles = [
        'User Id', 'First Name', 'Last Name', 'Email', 'Is Active',
        'Is Presenter', 'Is POC', 'Is Organiser']
    writer.writerow(csv_titles)
    for obj in users:
        try:
            row = [
                obj.id,
                obj.first_name,
                obj.last_name,
                obj.email,
                obj.is_active,
                Profile.is_presenter(obj),
                Profile.is_coordinator(obj),
                Profile.is_organiser(obj)]
            writer.writerow(row)
        except Exception:
            pass
    return response
