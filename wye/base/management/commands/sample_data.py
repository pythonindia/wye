# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from wye.organisations.models import Organisation, Location, State


NUMBER_OF_USERS = getattr(settings, "NUMBER_OF_USERS", 10)


class Command(BaseCommand):
    fake = Faker()

    @transaction.atomic
    def handle(self, *args, **options):
        self.fake.seed(4321)

        print('  Updating domain to localhost:8000')  # Update site url
        site = Site.objects.get_current()
        site.domain, site.name = 'localhost:8000', 'Local'
        site.save()

        print('  Creating Superuser')
        self.create_user(is_superuser=True, username='admin', email='admin@fossevents.in',
                         is_active=True, is_staff=True, first_name='Admin')

        print('  Creating sample users')
        for i in range(NUMBER_OF_USERS):
            self.create_user()
    def create_user(self, counter=None, **kwargs):
        params = {
            "first_name": kwargs.get('first_name', self.fake.first_name()),
            "last_name": kwargs.get('last_name', self.fake.last_name()),
            "username": kwargs.get('username', self.fake.user_name()),
            "email": kwargs.get('email', self.fake.email()),
            "is_active": kwargs.get('is_active', self.fake.boolean()),
            "is_superuser": kwargs.get('is_superuser', False),
            "is_staff": kwargs.get('is_staff', kwargs.get('is_superuser', self.fake.boolean())),
        }

        user, created = get_user_model().objects.get_or_create(**params)

        if params['is_superuser']:
            password = '123123'
            user.set_password(password)
            user.save()

            print("SuperUser created with username: {username} and password: {password}".format(
                username=params['username'], password=password)
            )

        return user
