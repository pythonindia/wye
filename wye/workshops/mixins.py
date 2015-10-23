from wye.profiles.models import Profile
from wye.base.emailer import send_mail


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
