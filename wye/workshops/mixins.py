from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from wye.base.constants import WorkshopStatus, FeedbackType
from wye.base.emailer import send_mail
from wye.profiles.models import Profile

from .models import Workshop, WorkshopFeedBack


class WorkshopAccessMixin(object):

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        workshop = Workshop.objects.get(id=pk)
        if workshop.requester not in self.request.user.organisation_users.all():
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
        if not (workshop.is_presenter(user) and workshop.is_organiser(user)):
            raise PermissionDenied
        return super(WorkshopFeedBackMixin, self).dispatch(request, *args, **kwargs)


class WorkshopRestrictMixin(object):
    """
    Mixin to restrict 
        - For organisation to add workshop if no feedback is shared.
        - For presenter to takeup workshop if no feedback is shared
    """

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        self.feedback_required = []
        usertype = self.user.profile.usertype

        if usertype.filter(display_name__icontains="tutor").exists():
            self.validate_presenter_feedback()
        elif usertype.filter(display_name__icontains="poc").exists():
            self.validate_organisation_feedback()

        if self.feedback_required:
            return HttpResponse(", ".join(map(str, self.feedback_required)))

        return super(WorkshopRestrictMixin, self).dispatch(request, *args, **kwargs)

    def validate_presenter_feedback(self):
        workshops = Workshop.objects.filter(
            presenter=self.user, status=WorkshopStatus.COMPLETED)

        for workshop in workshops:
            feedback = WorkshopFeedBack.objects.filter(
                workshop=workshop, feedback_type=FeedbackType.PRESENTER
            ).count()
            if feedback == 0:
                feedback_required.append(w)

    def validate_organisation_feedback():
        workshops = Workshop.objects.filter(
            presenter=user, status=WorkshopStatus.COMPLETED)

        for workshop in workshops:
            feedback = WorkshopFeedBack.objects.filter(
                workshop=workshop, feedback_type=FeedbackType.ORGANISATION
            ).count()
            if feedback == 0:
                feedback_required.append(w)


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

        all_email = []
        all_email.extend(org_user_emails)
        all_email.extend(all_presenter_email)
        all_email.extend(poc_admin_user)
        all_email = set(all_email)
        all_email = list(all_email.difference(exclude_emails))
        send_mail(all_email, context, self.email_dir)
