from django.db import models
from django.contrib.auth.models import User

from wye.base.constants import (
    FeedbackType,
    WorkshopAction,
    WorkshopLevel,
    WorkshopStatus,
)
from wye.regions.models import Location
from wye.base.models import TimeAuditModel
from wye.organisations.models import Organisation

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
        choices=WorkshopStatus.CHOICES, verbose_name="Current Status",
        default=WorkshopStatus.DRAFT)

    class Meta:
        db_table = 'workshops'

    def __str__(self):
        return '{}-{}'.format(self.requester, self.workshop_section)

    def is_presenter(self, user):
        return self.presenter.filter(pk=user.pk).exists()

    def is_organiser(self, user):
        return self.requester.user.filter(pk=user.pk).exists()

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
                'msg': 'Sorry, but it would seem that this \
                        workshop is already completed and hence \
                        won\'t be able to accept a presenter.'}

        action_map = {
            'opt-in': self.presenter.add,
            'opt-out': self.presenter.remove
        }
        message_map = {
            'opt-in': 'Assigned successfully.',
            'opt-out': 'Unassigned successfully.'
        }
        assigned = {
            'opt-in': True,
            'opt-out': False
        }
        action = kwargs.get('action')
        if assigned[action] and self.presenter.filter(pk=user.pk).exists():
            return {
                'status': False,
                'msg': 'Workshop has already been assigned.'
            }

        func = action_map.get(action)
        func(user)
        return {
            'status': True,
            'assigned': assigned[action],
            'msg': message_map[action]
        }

    def get_presenter_list(self):
        return [user.get_full_name() for user in self.presenter.all()]

    def get_tweet(self, context):
        workshop = self
        date = workshop.expected_date
        topic = workshop.workshop_section
        organization = workshop.requester
        workshop_url = context.get('workshop_url', None)
        message = "{} workshop at {} on {} confirmed! Details at {}".format(
            topic, organization, date, workshop_url)
        if len(message) >= 140:
            message = "{} workshop on {} confirmed! Details at {}".format(
                topic, date, workshop_url)

        return message


class WorkshopRatingValues(TimeAuditModel):
    '''
    Requesting Rating values -2, -1, 0 , 1, 2
    '''

    name = models.CharField(max_length=300)

    class Meta:
        db_table = 'workshop_vote_value'

    def __str__(self):
        return '{}'.format(self.name)

    @classmethod
    def get_questions(cls):
        return cls.objects.values('name', 'pk')


class WorkshopFeedBack(TimeAuditModel):
    '''
    Requesting for Feedback from requester and Presenter
    '''

    workshop = models.ForeignKey(Workshop)
    comment = models.TextField()
    feedback_type = models.PositiveSmallIntegerField(
        choices=FeedbackType.CHOICES, verbose_name="User_type")

    class Meta:
        db_table = 'workshop_feedback'

    def __str__(self):
        return '{}'.format(self.workshop)

    @classmethod
    def save_feedback(cls, user, workshop_id, **kwargs):
        workshop = Workshop.objects.get(pk=workshop_id)
        presenter = workshop.is_presenter(user)
        organiser = workshop.is_organiser(user)
        comment = kwargs.get('comment', '')
        del kwargs['comment']

        if presenter:
            feedback_type = FeedbackType.PRESENTER
        elif organiser:
            feedback_type = FeedbackType.ORGANISATION

        workshop_feedback = cls.objects.create(
            workshop=workshop,
            comment=comment,
            feedback_type=feedback_type
        )
        WorkshopVoting.save_rating(workshop_feedback, **kwargs)


class WorkshopVoting(TimeAuditModel):
    workshop_feedback = models.ForeignKey(
        WorkshopFeedBack, related_name='workshop_feedback')
    workshop_rating = models.ForeignKey(
        WorkshopRatingValues, related_name='workshop_rating')
    rating = models.IntegerField()

    class Meta:
        db_table = 'workshop_votes'

    def __str__(self):
        return '{}-{}-{}'.format(self.workshop_feedback,
                                 self.workshop_rating,
                                 self.rating)

    @classmethod
    def save_rating(cls, workshop_feedback, **kwargs):
        object_list = [
            cls(workshop_feedback=workshop_feedback,
                workshop_rating_id=int(k), rating=v)
            for k, v in kwargs.iteritems()
        ]

        cls.objects.bulk_create(object_list)
