from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
# from django.core.validators import MaxValueValidator
from django.db import models
# from django.template import loader
# from wye.profiles.models import Profile
# from wye.simple_history.models import HistoricalRecords
from wye.base.constants import (
    FeedbackType,
    WorkshopLevel,
    WorkshopStatus,
    YesNO,
    WorkshopAudience
)
# from wye.base.emailer_html import send_email_to_id
from wye.base.models import TimeAuditModel
from wye.organisations.models import Organisation


class WorkshopSections(TimeAuditModel):
    '''
    python2, Python3, Django, Flask, Gaming
    '''
    name = models.CharField(max_length=300, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'workshop_section'

    def __str__(self):
        return '{}'.format(self.name)


class Workshop(TimeAuditModel):
    no_of_participants = models.PositiveIntegerField(choices=(
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
        (60, 60),))
    expected_date = models.DateField()
    description = models.TextField()
    requester = models.ForeignKey(
        Organisation, related_name='workshop_requester')
    presenter = models.ManyToManyField(User, related_name='workshop_presenter')
    # location = models.ForeignKey(Location, related_name='workshop_location')
    workshop_level = models.PositiveSmallIntegerField(
        choices=WorkshopLevel.CHOICES, verbose_name="Workshop Level")
    workshop_section = models.ForeignKey(WorkshopSections)
    number_of_volunteers = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True)
    volunteer = models.ManyToManyField(User, related_name='workshop_volunteer')
    is_active = models.BooleanField(default=True)
    status = models.PositiveSmallIntegerField(
        choices=WorkshopStatus.CHOICES, verbose_name="Current Status",
        default=WorkshopStatus.REQUESTED)
    travel_reimbursement = models.PositiveSmallIntegerField(
        choices=YesNO.CHOICES,
        verbose_name="Travel Reimbursement Support",
        default=YesNO.NO)
    hotel_reimbursement = models.PositiveSmallIntegerField(
        choices=YesNO.CHOICES,
        verbose_name="Stay Reimbursement Support",
        default=YesNO.NO)
    budget = models.CharField(max_length=5, null=True)
    reimbursement_mode = models.TextField(null=True)
    tutor_reimbursement_flag = models.PositiveSmallIntegerField(
        choices=YesNO.CHOICES,
        verbose_name=" Do you need Travel/Stay reimbursement ?",
        default=YesNO.NO)
    comments = models.TextField()
    target_audience = models.PositiveSmallIntegerField(
        choices=WorkshopAudience.CHOICES, verbose_name="Audience",
        default=WorkshopAudience.BE_FINAL_YEAR)
    student_attended = models.ManyToManyField(User, related_name='workshop_attended')

    class Meta:
        db_table = 'workshops'

    def __str__(self):
        return '{}-{}'.format(self.requester, self.workshop_section)

    def save(self, force_insert=False, force_update=False, using=None):
        super(Workshop, self).save(force_insert, force_update, using)

    def is_presenter(self, user):
        return self.presenter.filter(pk=user.pk).exists()

    def is_organiser(self, user):
        return self.requester.user.filter(pk=user.pk).exists()

    def manage_action(self, user, **kwargs):
        actions = {
            'accept': ("opt-in", self.assign_me),
            'reject': ("opt-out", self.assign_me),
            'decline': (WorkshopStatus.REQUESTED, self.set_status),
            'publish': (WorkshopStatus.REQUESTED, self.set_status),
            'hold': (WorkshopStatus.HOLD, self.set_status),
            'assign': "",
            'opt-in-as-volunteer': '',
            'opt-out-as-volunteer': ''
        }
        if kwargs.get('action') not in actions:
            return {
                'status': False,
                'msg': 'Action not allowed'
            }

        action, func = actions.get(kwargs.get('action'))
        kwargs["action"] = action
        return func(user, **kwargs)

    def set_status(self, user, **kwargs):
        self.status = kwargs.get('action')
        presenter_list = self.presenter.all()
        for u in presenter_list:
            self.presenter.remove(u)
        if kwargs.get('action') == WorkshopStatus.DECLINED:
            self.is_active = False
        else:
            self.is_active = True
        self.save()
        return {
            'status': True,
            'msg': 'Workshop successfully updated.'}

    # @validate_action_param(WorkshopAction.ACTIVE)
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

    # @validate_action_param(WorkshopAction.ASSIGNME)
    # @validate_assignme_action
    def assign_me(self, user, **kwargs):
        """
        Method to assign workshop by presenter self.
        """

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
            # This save has been added as fail safe
            # once the logic is consolidated may be
            # it can be removed
            self.status = WorkshopStatus.ACCEPTED
            self.save()
            return {
                'status': False,
                'msg': 'Workshop has already been assigned.'
            }

        func = action_map.get(action)
        func(user)

        if action == 'opt-out':
            self.number_of_volunteers = 0
            self.volunteer.clear()

        if self.presenter.count() > 0:
            self.status = WorkshopStatus.ACCEPTED
        else:
            self.status = WorkshopStatus.REQUESTED
        self.save()

        return {
            'status': True,
            'assigned': assigned[action],
            'msg': message_map[action],
            'notify': True
        }

    def get_presenter_list(self):
        return [user.get_full_name() for user in self.presenter.all()]

    def get_tweet(self, context):
        workshop = self
        try:
            date = workshop.expected_date.strftime('%d-%m-%Y')
        except:
            date = workshop.expected_date

        topic = workshop.workshop_section
        organization = workshop.requester
        location = workshop.requester.location
        workshop_url = context.get('workshop_url', None)
        message = "{} workshop at {} on {} confirmed! Details: {}".format(
            topic, organization, date, workshop_url)
        if len(message) >= 140:
            message = "{} workshop at {} on {} confirmed! Details: {}".format(
                topic, location, date, workshop_url)
        if len(message) >= 140:
            message = "{} workshop on {} confirmed! Details :{}".format(
                topic, date, workshop_url)

        return message

        def opt_in_as_volunteer(self):
            pass

        def opt_out_as_volunteer(self):
            pass


class WorkshopRatingValues(TimeAuditModel):
    '''
    Requesting Rating values -2, -1, 0 , 1, 2
    '''

    name = models.CharField(max_length=300)
    feedback_type = models.PositiveSmallIntegerField(
        choices=FeedbackType.CHOICES, verbose_name="User_type")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'workshop_vote_value'

    def __str__(self):
        return '{}-{}'.format(self.id, self.feedback_type)

    @classmethod
    def get_questions(cls, feedback_type):
        if feedback_type:
            return cls.objects.filter(feedback_type=feedback_type)
        return None


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
        kwargs.pop('csrfmiddlewaretoken', None)
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
                workshop_rating_id=int(k.split('-')[0]), rating=v[0])
            for k, v in kwargs.items()
        ]
        cls.objects.bulk_create(object_list)

