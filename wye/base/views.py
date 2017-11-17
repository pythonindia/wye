from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import uuid
from wye.organisations.models import Organisation
from wye.profiles.models import Profile
from wye.workshops.models import Workshop

from .constants import WorkshopStatus


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        organisationObj = Organisation.objects.filter(active=True)
        workshopObj = Workshop.objects.filter(is_active=True)
        context['organisation_registered_count'] = organisationObj.count()
        context['completed_workshop_count'] = workshopObj.filter(
            status=WorkshopStatus.COMPLETED).count()
        workshopObj = workshopObj.filter(status__in=[
            WorkshopStatus.REQUESTED,
            WorkshopStatus.ACCEPTED,
            WorkshopStatus.DECLINED])
        workshop_list = Workshop.objects.filter(
            is_active=True
        ).filter(
            status__in=[WorkshopStatus.REQUESTED, WorkshopStatus.ACCEPTED]
        ).order_by('expected_date')
        context['requested_workshop_count'] = workshopObj.count()
        context['tutor_registered_count'] = Profile.objects.filter(
            usertype__slug="tutor").count()
        context['upcoming_workshops'] = workshop_list
        return context


def verify_user_profile(f):
    '''
    This decorator check  whether the user are valid for certain views
    '''
    def wrap(request, *args, **kwargs):
        user_profile, created = Profile.objects.get_or_create(
            user__id=request.user.id)
        if not user_profile.is_profile_filled:
            return HttpResponseRedirect(
                '/profile/{}/edit'.format(request.user.username))
        return f(request, *args, **kwargs)
    return wrap


def get_username(email):
    """
    Returns a UUID-based 'random' and unique username.

    This is required data for user models with a username field.
    """
    # uuid_str = str(uuid.uuid4())
    username = email.split("@")[0]
    # uuid_str = uuid_str[:30 - len(username)]
    # print(username)
    return username


def add_user_create_reset_password_link(
        first_name, last_name, email, mobile, usertype):
    user, created = User.objects.get_or_create(email=email)
    if created:
        user.first_name = first_name
        user.last_name = last_name
        user.username = get_username(email)
        user.is_active = True
        user.set_password('123456')
        user.save()
        print("After creating user")
        print(user.username)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.usertype.add(usertype)
        profile.mobile = mobile
        profile.save()
    return user, created
