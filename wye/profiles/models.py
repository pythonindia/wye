# from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

from wye.workshops.models import WorkshopSections


class UserType(models.Model):
    '''
    USER_TYPE = ['Tutor', 'POC', 'admin']
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
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    # the slug fields become the username and should be unique for each user
    slug = models.CharField(max_length=100, unique=True)
    mobile = models.CharField(max_length=10)
    usertype = models.ForeignKey(UserType)
    interested_sections = models.ManyToManyField(WorkshopSections)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return '{} {}'.format(self.user, self.slug)
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         token, created = Token.objects.get_or_create(user=instance)
