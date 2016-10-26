import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from wye.base.constants import WorkshopStatus
from wye.organisations.models import Organisation
# from wye.profiles.models import Profile
from wye.workshops.models import Workshop


@login_required
def index(request, days):
    if not request.user.is_staff:
        return ""
    d = datetime.datetime.now() - datetime.timedelta(days=int(days))
    organisations = Organisation.objects.filter(
        active=True).filter(created_at__gte=d)
    workshops = Workshop.objects.filter(
        is_active=True).filter(
        expected_date__gte=d).filter(
        expected_date__lte=datetime.datetime.now()).filter(
        status__in=[WorkshopStatus.COMPLETED,
                    WorkshopStatus.FEEDBACK_PENDING]).order_by('expected_date')
    # profiles = Profile.objects.filter(user__date_joined__gte=d)
    no_of_participants = 0
    tutors = []
    regions_based_dict = {}
    state_based_dict = {}
    for w in workshops:
        no_of_participants = no_of_participants + w.no_of_participants
        tutors.extend([presenter for presenter in w.presenter.all()])
        regions_based_dict.setdefault(w.location.id, [w.location.name, 0, 0])
        regions_based_dict[w.location.id][1] = regions_based_dict[w.location.id][1] + 1
        regions_based_dict[w.location.id][2] = regions_based_dict[w.location.id][2] + w.no_of_participants
        state_based_dict.setdefault(w.location.state.id, [w.location.state.name, 0, 0])
        state_based_dict[w.location.state.id][1] = state_based_dict[w.location.state.id][1] + 1
        state_based_dict[w.location.state.id][2] = state_based_dict[w.location.state.id][2] + +w.no_of_participants
    template_name = 'reports/index.html'
    context_dict = {}
    context_dict['organisations'] = organisations
    context_dict['workshops'] = workshops
    context_dict['tutors'] = tutors
    context_dict['state_based_dict'] = state_based_dict
    context_dict['regions_based_dict'] = regions_based_dict
    # context_dict['profiles'] = profiles
    context_dict['no_of_participants'] = no_of_participants
    context_dict['date'] = d
    workshops = Workshop.objects.filter(
        is_active=True)

    return render(request, template_name, context_dict)
