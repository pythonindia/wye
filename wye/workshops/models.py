from django.contrib.auth.models import User
from django.db import models

from wye.base.models import TimeAuditModel
from wye.organisations.models import Organisations, Location


class WorkshopLevel(TimeAuditModel):
    '''
    Beginners, Intermediate, Advance
    '''
    name = models.CharField(max_length=300, unique=True)

    class Meta:
        db_table = 'workshop_level'

    def __str__(self):
        return '{}' % (self.name)


class WorkshopSections(TimeAuditModel):
    '''
    python2, Python3, Django, Flask, Gaming
    '''
    name = models.CharField(max_length=300, unique=True)

    class Meta:
        db_table = 'workshop_section'

    def __str__(self):
        return '{}' % (self.name)


class Workshop(TimeAuditModel):
    no_of_participants = models.IntegerField()
    expected_date = models.DateField()
    description = models.TextField()
    requester = models.ForeignKey(
        Organisations, related_name='workshop_requester')
    presenter = models.ManyToManyField(User, related_name='workshop_presenter')
    location = models.ForeignKey(Location, related_name='workshop_location')
    workshop_level = models.ForeignKey(WorkshopLevel)
    workshop_section = models.ForeignKey(WorkshopSections)

    class Meta:
        db_table = 'workshops'

    def __str__(self):
        return '{}-{}' % (self.requester, self.presenter)


class WorkshopRatingValues(TimeAuditModel):
    '''
    Requesting Rating values -2, -1, 0 , 1, 2
    '''
    value = models.IntegerField()
    name = models.CharField(max_length=300)

    class Meta:
        db_table = 'workshop_rating_value'

    def __str__(self):
        return '{}-{}' % (self.value, self.name)


class WorkshopFeedBack(TimeAuditModel):
    '''
    Requesting for Feedback from requester and Presenter
    '''
    requester_rating = models.ForeignKey(WorkshopRatingValues)
    presenter_rating = models.ForeignKey(WorkshopRatingValues)
    requester_comment = models.TextField()
    presenter_comment = models.TextField()
    workshop = models.ForeignKey(Workshop)

    class Meta:
        db_table = 'workshop_feedback'

    def __str__(self):
        return '{}-{}-{}' % (self.workshop,
                             self.requester_rating,
                             self.presenter_rating)
