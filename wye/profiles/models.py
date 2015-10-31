
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
# from django.conf import settings
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from django.utils.functional import cached_property
from slugify import slugify

from wye.base.constants import WorkshopStatus
from wye.regions.models import Location
from wye.workshops.models import Workshop, WorkshopSections


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
        return '{} - {}'.format(self.slug, self.display_name)


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    mobile = models.CharField(max_length=10)
    usertype = models.ManyToManyField(UserType)
    interested_sections = models.ManyToManyField(WorkshopSections)
    interested_locations = models.ManyToManyField(Location)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return '{} {}'.format(self.user, self.slug)

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
        pass

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


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         token, created = Token.objects.get_or_create(user=instance)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User, dispatch_uid='create_user_profile')
