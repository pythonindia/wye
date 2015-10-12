from django.contrib.auth.models import User
from django.db import models

from wye.base.constants import OrganisationType
from wye.base.models import TimeAuditModel


# class OrganisationType(TimeAuditModel):
#     '''
#     College, Orgnaisation , Student Groups
#     '''
#     name = models.CharField(max_length=300, unique=True)
#
#     class Meta:
#         db_table = 'organisation_types'
#
#     def __str__(self):
#         return '{}'.format(self.name)
class State(TimeAuditModel):
    '''

    '''
    name = models.CharField(max_length=300, unique=True)

    class Meta:
        db_table = 'states'

    def __str__(self):
        return '{}'.format(self.name)


class Location(TimeAuditModel):
    '''
    '''
    name = models.CharField(max_length=300, unique=True)
    state = models.ForeignKey(State)

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return '{}'.format(self.name)


class Organisation(TimeAuditModel):
    organisation_type = models.PositiveSmallIntegerField(
        choices=OrganisationType.CHOICES, verbose_name="Organisation Type")
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    location = models.ForeignKey(Location)
    organisation_role = models.CharField(max_length=300)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'organisations'

    def __str__(self):
        return '{}-{}-{}'.format(self.name,
                                 self.organisation_type, self.location)
