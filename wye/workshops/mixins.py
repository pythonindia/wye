from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect, JsonResponse

from wye.base.constants import WorkshopStatus, FeedbackType
from wye.base.emailer import send_mail
from wye.organisations.models import Organisation
from wye.profiles.models import Profile
from wye.regions.models import RegionalLead

from .models import Workshop, WorkshopFeedBack


class WorkshopAccessMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        workshop = Workshop.objects.get(id=pk)

        is_admin = Profile.is_admin(user)
        is_lead = (Profile.is_regional_lead(user) and
                   RegionalLead.is_regional_lead(user, workshop.location))
        is_presenter = (Profile.is_organiser(user) and
                        user in workshop.requester.user.all())

        if not (is_admin or is_lead or is_presenter):
            raise PermissionDenied
        return super(WorkshopAccessMixin, self).dispatch(request, *args, **kwargs)


class WorkshopFeedBackMixin(object):
    """
    Restrict access to feedback url if
    - Workshop is not completed
    - If the user accessing the url is not presenter or
      organiser
    """

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        workshop = Workshop.objects.get(id=pk)
        user = self.request.user

        if workshop.status != WorkshopStatus.COMPLETED:
            raise Http404
        if not (workshop.is_presenter(user) or workshop.is_organiser(user)):
            raise PermissionDenied
        return super(WorkshopFeedBackMixin, self).dispatch(request, *args, **kwargs)


class WorkshopRestrictMixin(object):
    """
    Mixin to restrict
        - For organisation to add workshop if no feedback is shared.
        - For presenter to takeup workshop if no feedback is shared
    """

    allow_presenter = False

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.feedback_required = []

        # check if user is tutor
        if Profile.is_presenter(self.user) and self.allow_presenter:
            self.validate_presenter_feedback()
        elif (Profile.is_organiser(self.user) and
                Organisation.list_user_organisations(self.user).exists()):
            # if user is from organisation
            self.validate_organisation_feedback()
        elif (Profile.is_regional_lead(self.user) or
                Profile.is_admin(self.user)):
            pass  # don't restrict lead and admin
        else:
            raise PermissionDenied

        if self.feedback_required:
            return self.return_response(request)
        return super(WorkshopRestrictMixin, self).dispatch(request, *args, **kwargs)

    def validate_presenter_feedback(self):
        workshops = Workshop.objects.filter(
            presenter=self.user, status=WorkshopStatus.COMPLETED)

        for workshop in workshops:
            feedback = WorkshopFeedBack.objects.filter(
                workshop=workshop, feedback_type=FeedbackType.PRESENTER
            ).count()
            if feedback == 0:
                self.feedback_required.append(workshop)

    def validate_organisation_feedback(self):
        workshops = Workshop.objects.filter(
            requester__user=self.user, status=WorkshopStatus.COMPLETED)

        for workshop in workshops:
            feedback = WorkshopFeedBack.objects.filter(
                workshop=workshop, feedback_type=FeedbackType.ORGANISATION
            ).count()
            if feedback == 0:
                self.feedback_required.append(workshop)

    def return_response(self, request):
        msg = "Please complete the feeback for %s" % (
            ", ".join(map(str, self.feedback_required)))

        # return json for ajax request
        if request.is_ajax():
            return JsonResponse({"status": False, "msg": msg})

        messages.error(request, msg)
        return HttpResponseRedirect(reverse('workshops:workshop_list'))


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
        ).values_list('email', flat=True)

        all_email = []
        all_email.extend(org_user_emails)
        all_email.extend(all_presenter_email)
        all_email.extend(poc_admin_user)
        all_email.extend(region_interested_member)
        all_email = set(all_email)
        all_email = list(all_email.difference(exclude_emails))
        send_mail(all_email, context, self.email_dir)
