from django.contrib.auth.models import User
from django.db import models

from wye.base.models import TimeAuditModel


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
        return '{}, {}'.format(self.name, self.state.name)


class RegionalLead(models.Model):
    location = models.ForeignKey(Location)
    leads = models.ManyToManyField(User)

    class Meta:
        db_table = 'regional_lead'
        verbose_name = 'RegionalLead'
        verbose_name_plural = 'RegionalLeads'

    def __str__(self):
        return '{}'.format(self.location)

    @property
    def get_count_of_leads(self):
        return self.leads.count()

    @classmethod
    def is_regional_lead(cls, user, location):
        return cls.objects.filter(
            leads=user, location=location).exists()
