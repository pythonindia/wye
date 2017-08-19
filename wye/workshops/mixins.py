# from django.contrib import messages
# from django.core.exceptions import PermissionDenied
# from django.core.urlresolvers import reverse
# from django.http import Http404
from django.http import HttpResponseForbidden
# from django.http import HttpResponseRedirect, JsonResponse
# from django.shortcuts import render

# from wye.base.constants import WorkshopStatus, FeedbackType
from wye.base.emailer import send_mail
# from wye.organisations.models import Organisation
from wye.profiles.models import Profile
from wye.regions.models import RegionalLead

from .models import Workshop


class WorkshopAccessMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        workshop = Workshop.objects.get(id=pk)
        is_admin = Profile.is_admin(user)
        is_lead = (Profile.is_regional_lead(user) and
                   RegionalLead.is_regional_lead(user, workshop.location))
        is_organiser = (Profile.is_organiser(user) and
                        user in workshop.requester.user.all())

        if not (is_admin or is_lead or is_organiser):
            return HttpResponseForbidden("Not sufficent permission")
        return super(WorkshopAccessMixin, self).dispatch(
            request, *args, **kwargs)


class WorkshopEmailMixin(object):

    def send_mail_to_presenter(self, user, context):
        """
        Send email to presenter.
        @param user: Is user object
        @param context: Is dict of data required by email template.
        """

        # Send email to presenter
        return send_mail([user.email], context, self.email_dir)

    def send_mail_to_group(self, context, exclude_emails=None):
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
            user_type=['Collage POC', 'admin']
        ).values_list('email', flat=True)
        # Org user email
        org_user_emails = self.object.requester.user.filter(
            is_active=True
        ).values_list('email', flat=True)
        # all presenter if any
        all_presenter_email = self.object.presenter.values_list(
            'email', flat=True
        )
        # List of tutor who have shown interest in that location
        region_interested_member = Profile.objects.filter(
            interested_locations=self.object.requester.location,
            usertype__slug='tutor'
        ).values_list('user__email', flat=True)

        all_email = []
        all_email.extend(org_user_emails)
        all_email.extend(all_presenter_email)
        all_email.extend(poc_admin_user)
        all_email.extend(region_interested_member)
        all_email = set(all_email)
        all_email = list(all_email.difference(exclude_emails))
        send_mail(all_email, context, self.email_dir)
