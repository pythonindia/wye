from django.contrib.auth.models import User
from django.db import models

from wye.base.constants import WorkshopStatus, WorkshopLevel, WorkshopAction
from wye.base.models import TimeAuditModel
from wye.organisations.models import Organisation, Location

from .decorators import validate_action_param

# class WorkshopLevel(TimeAuditModel):
#     '''
#     Beginners, Intermediate, Advance
#     '''
#     name = models.CharField(max_length=300, unique=True)
#
#     class Meta:
#         db_table = 'workshop_level'
#
#     def __str__(self):
#         return '{}'.format(self.name)
#
#
class WorkshopSections(TimeAuditModel):
    '''
    python2, Python3, Django, Flask, Gaming
    '''
    name = models.CharField(max_length=300, unique=True)

    class Meta:
        db_table = 'workshop_section'

    def __str__(self):
        return '{}'.format(self.name)


class Workshop(TimeAuditModel):
    no_of_participants = models.PositiveIntegerField()
    expected_date = models.DateField()
    description = models.TextField()
    requester = models.ForeignKey(
        Organisation, related_name='workshop_requester')
    presenter = models.ManyToManyField(User, related_name='workshop_presenter')
    location = models.ForeignKey(Location, related_name='workshop_location')
    workshop_level = models.PositiveSmallIntegerField(
        choices=WorkshopLevel.CHOICES, verbose_name="Workshop Level")
    workshop_section = models.ForeignKey(WorkshopSections)
    is_active = models.BooleanField(default=True)
    status = models.PositiveSmallIntegerField(
        choices=WorkshopStatus.CHOICES, verbose_name="Current Status")

    class Meta:
        db_table = 'workshops'

    def __str__(self):
        return '{}-{}'.format(self.requester, self.workshop_section)

    @validate_action_param(WorkshopAction.ACTIVE)
    def toggle_active(self, user, **kwargs):
        """
        Helper method to toggle is_active for the model.
        """

        action_map = {'active': True, 'deactive': False}
        action = kwargs.get('action')
        self.is_active = action_map.get(action)
        self.save()
        return {
            'status': True,
            'msg': 'Workshop successfully updated.'}

    @validate_action_param(WorkshopAction.ASSIGNME)
    def assign_me(self, user, **kwargs):
        """
        Method to assign workshop by presenter self.
        """

        # if workshop completed don't accept
        # presenter.
        if self.status == WorkshopStatus.COMPLETED:
            return {
                'status': False, 
                'msg': 'Workshop completed.'}

        action_map = {
            'opt-in': self.presenter.add, 
            'opt-out': self.presenter.remove}
        message_map = {
            'opt-in': 'Assigned succesfully.',
            'opt-out': 'Unassigned Successfully.'
        }
        action = kwargs.get('action')
        func = action_map.get(action)
        func(user)
        return {
            'status': True, 
            'msg': message_map[action]}


class WorkshopRatingValues(TimeAuditModel):
    '''
    Requesting Rating values -2, -1, 0 , 1, 2
    '''
    value = models.IntegerField()
    name = models.CharField(max_length=300)

    class Meta:
        db_table = 'workshop_vote_value'

    def __str__(self):
        return '{}-{}' % (self.value, self.name)


class WorkshopVoting(TimeAuditModel):
    requester_rating = models.ForeignKey(
        WorkshopRatingValues, related_name='requester_rating')
    presenter_rating = models.ForeignKey(
        WorkshopRatingValues, related_name='presenter_rating')
    workshop = models.ForeignKey(Workshop)

    class Meta:
        db_table = 'workshop_votes'

    def __str__(self):
        return '{}-{}-{}' % (self.workshop,
                             self.requester_rating,
                             self.presenter_rating)


class WorkshopFeedBack(TimeAuditModel):
    '''
    Requesting for Feedback from requester and Presenter
    '''
    requester_comment = models.TextField()
    presenter_comment = models.TextField()
    workshop = models.ForeignKey(Workshop)

    class Meta:
        db_table = 'workshop_feedback'

    def __str__(self):
        return '{}-{}-{}' % (self.workshop,
                             self.requester_rating,
                             self.presenter_rating)
