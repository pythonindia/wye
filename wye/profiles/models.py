import json

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.functional import cached_property

from dateutil.rrule import rrule, MONTHLY
from slugify import slugify
from wye.base.constants import WorkshopStatus
from wye.regions.models import Location
from wye.workshops.models import Workshop, WorkshopSections


# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
class UserType(models.Model):
    '''
    USER_TYPE = ['Tutor', 'Regional Lead', 'College POC','admin']
    '''
    slug = models.CharField(max_length=100,
                            verbose_name="slug")
    display_name = models.CharField(
        max_length=300, verbose_name="Display Name")
    active = models.BooleanField(default=1)

    class Meta:
        db_table = 'users_type'
        verbose_name = 'UserType'
        verbose_name_plural = 'UserTypes'
        ordering = ('-id',)

    def __str__(self):
        return '{}'.format(self.display_name)


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    mobile = models.CharField(max_length=10, blank=False, null=True)
    is_mobile_visible = models.BooleanField(default=False)
    is_email_visible = models.BooleanField(default=False)
    usertype = models.ManyToManyField(UserType, null=True)
    interested_sections = models.ManyToManyField(WorkshopSections)
    interested_locations = models.ManyToManyField(Location)
    location = models.ForeignKey(
        Location, related_name="user_location", null=True)
    github = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    googleplus = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    slideshare = models.URLField(null=True, blank=True)
    picture = models.ImageField(
        upload_to='images/', default='images/newuser.png')

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return '{} {}'.format(self.user, self.slug)

    @property
    def is_profile_filled(self):
        if self.location:
            return True
        return False

    @cached_property
    def slug(self):
        return slugify(self.user.username, only_ascii=True)

    @property
    def get_workshop_details(self):
        return Workshop.objects.filter(presenter=self.user).order_by('-id')

    @property
    def get_workshop_completed_count(self):
        return len([x for x in
                    self.get_workshop_details if x.status == WorkshopStatus.COMPLETED])

    @property
    def get_workshop_upcoming_count(self):
        return len([x for x in
                    self.get_workshop_details if x.status == WorkshopStatus.ACCEPTED])

    @property
    def get_total_no_of_participants(self):
        return sum([x.no_of_participants for x in
                    self.get_workshop_details if x.status == WorkshopStatus.COMPLETED])

    @property
    def get_last_workshop_date(self):
        pass

    @property
    def get_avg_workshop_rating(self):
        # TODO: Complete!
        return 0

    @staticmethod
    def get_user_with_type(user_type=None):
        """
        Would return user with user type list in argument.
        Eg Collage POC, admin etc
        """
        return User.objects.filter(
            profile__usertype__display_name__in=user_type
        )

    @property
    def get_user_type(self):
        return [x.slug for x in self.usertype.all()]

    @property
    def get_interested_locations(self):
        return [x.name for x in self.interested_locations.all()]

    @property
    def get_graph_data(self):
        sections = WorkshopSections.objects.all()
        workshops = Workshop.objects.filter(
            presenter=self.user,
            status=WorkshopStatus.COMPLETED
        )
        if workshops:
            max_workshop_date = workshops.aggregate(
                models.Max('expected_date'))['expected_date__max']
            min_workshop_date = workshops.aggregate(
                models.Min('expected_date'))['expected_date__min']
            data = []
            if max_workshop_date and min_workshop_date:
                dates = [dt for dt in rrule(
                    MONTHLY, dtstart=min_workshop_date, until=max_workshop_date)]
                if dates:
                    for section in sections:
                        values = []
                        for d in dates:
                            y = workshops.filter(
                                expected_date__year=d.year,
                                expected_date__month=d.month,
                                workshop_section=section.pk).count()
                            values.append(
                                {'x': "{}-{}".format(d.year, d.month), 'y': y})
                        data.append({'key': section.name, 'values': values})
                    return json.dumps(data)
                else:
                    return []
            else:
                return []
        else:
            return []

    @classmethod
    def is_presenter(cls, user):
        return user.profile.usertype.filter(slug__iexact="tutor").exists()

    @classmethod
    def is_organiser(cls, user):
        return user.profile.usertype.filter(slug__icontains="poc").exists()

    @classmethod
    def is_regional_lead(cls, user):
        return user.profile.usertype.filter(slug__iexact="lead").exists()

    @classmethod
    def is_admin(cls, user):
        return user.profile.usertype.filter(slug__iexact="admin").exists()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(
    create_user_profile, sender=User, dispatch_uid='create_user_profile')
