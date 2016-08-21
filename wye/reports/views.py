from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wye.organisations.models import Organisation
from wye.workshops.models import Workshop
from wye.profiles.models import Profile
import datetime
from wye.base.constants import WorkshopStatus


@login_required
def index(request, days):
    print(request.user.is_staff)
    if not request.user.is_staff:
        return ""
    d = datetime.datetime.now() - datetime.timedelta(days=int(days))
    organisations = Organisation.objects.filter(
        active=True).filter(created_at__gte=d)
    workshops = Workshop.objects.filter(
        is_active=True).filter(
        expected_date__gte=d).filter(
        expected_date__lt=datetime.datetime.now()).filter(
        status__in=[WorkshopStatus.COMPLETED,
                    WorkshopStatus.FEEDBACK_PENDING]).order_by('expected_date')
    profiles = Profile.objects.filter(user__date_joined__gte=d)
    no_of_participants = sum([w.no_of_participants for w in workshops])
    template_name = 'reports/index.html'
    context_dict = {}
    context_dict['organisations'] = organisations
    context_dict['workshops'] = workshops
    context_dict['profiles'] = profiles
    context_dict['no_of_participants'] = no_of_participants
    context_dict['date'] = d
    workshops = Workshop.objects.filter(
        is_active=True)

    return render(request, template_name, context_dict)
