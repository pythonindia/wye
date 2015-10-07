from django.db import models

from wye.base.models import TimeAuditModel


class OrganisationType(TimeAuditModel):
    '''
    College, Orgnaisation , Student Groups
    '''
    name = models.CharField(max_length=300, unique=True)

    class Meta:
        db_table = 'organisation_types'

    def __str__(self):
        return '{}' % (self.name)


class State(TimeAuditModel):
    '''

    '''
    name = models.CharField(max_length=300, unique=True)

    class Meta:
        db_table = 'states'

    def __str__(self):
        return '{}' % (self.name)


class Location(TimeAuditModel):
    '''
    '''
    name = models.CharField(max_length=300, unique=True)
    state = models.ForeignKey(State)

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return '{}' % (self.name)


class Organisation(TimeAuditModel):
    organisation_type = models.ForeignKey(OrganisationType)
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    location = models.ForeignKey(Location)
    organisation_role = models.CharField(max_length=300)

    class Meta:
        db_table = 'organisations'

    def __str__(self):
        return '{}-{}-{}' % (self.name, self.organisation_type, self.location)
