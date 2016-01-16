from django.contrib.auth.models import User
from django.db import models

from wye.base.constants import OrganisationType
from wye.base.models import AuditModel
from wye.regions.models import Location


class Organisation(AuditModel):
    organisation_type = models.PositiveSmallIntegerField(
        choices=OrganisationType.CHOICES, verbose_name="organisation type")
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    location = models.ForeignKey(Location)
    organisation_role = models.CharField(
        max_length=300, verbose_name="Your position in organisation")
    user = models.ManyToManyField(User, related_name='organisation_users')
    active = models.BooleanField(default=True)

    @classmethod
    def list_user_organisations(cls, user):
        return cls.objects.filter(user=user, active=True)

    @property
    def get_organisation_user_list(self):
        return self.user.all()

    def toggle_active(self, logged_user, **kwargs):
        """
        Helper method to toggle is_active for the model.
        """

        action_map = {'active': True, 'deactive': False}
        action = kwargs.get('action')
        # check if user is only poc for the organisation
        self.user.remove(logged_user)
        if not self.user:
            # if there are no more poc for this organisation disable it
            # else Organisation will be active
            self.is_active = action_map.get(action)
        self.save()
        return {
            'status': True,
            'msg': 'Organisation disabled'}

    class Meta:
        db_table = 'organisations'

    def __str__(self):
        return '{}-{}-{}'.format(self.name,
                                 self.organisation_type, self.location)
