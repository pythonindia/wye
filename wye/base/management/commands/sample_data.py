# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Faker
from wye.organisations.models import Organisation
from wye.profiles.models import UserType
from wye.regions.models import Location, State
from wye.workshops.models import WorkshopSections


NUMBER_OF_USERS = getattr(settings, "NUMBER_OF_USERS", 10)
NUMBER_OF_LOCATIONS = getattr(settings, "NUMBER_OF_LOCATIONS", 10)
NUMBER_OF_ORGANISATIONS = getattr(settings, "NUMBER_OF_ORGANISATIONS", 10)
NUMBER_OF_WORKSHOP_SECTIONS = getattr(
    settings, "NUMBER_OF_WORKSHOP_SECTIONS", 5)


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
        email = 'admin@pythonexpress.in'
        self.create_user(is_superuser=True, username='admin', email=email,
                         is_active=True, is_staff=True, first_name='Admin')

        print('  Creating sample users')
        for i in range(NUMBER_OF_USERS):
            self.create_user()

        print('  Creating sample locations')
        self.create_locations(counter=NUMBER_OF_LOCATIONS)

        print('  Creating sample organisations')
        self.create_organisations(counter=NUMBER_OF_ORGANISATIONS)

        print('  Creating sample workshop sections')
        self.create_workshop_sections(counter=NUMBER_OF_WORKSHOP_SECTIONS)
        print('  Creating sample User Type sections')
        self.create_user_type(counter=NUMBER_OF_WORKSHOP_SECTIONS)

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

    def create_locations(self, counter=None):
        for i in range(counter):
            state, updated = State.objects.update_or_create(
                name=self.fake.state())
            Location.objects.update_or_create(
                name=self.fake.city(), state=state)

    def create_user_type(self, counter=None):
        user_type_tuple = [
            ('tutor', 'Tutor'),
            ('lead', 'Regional Lead'),
            ('poc', 'College POC'),
            ('admin', 'admin')]
        for i in user_type_tuple:
            obj, updated = UserType.objects.update_or_create(
                slug=i[0])
            obj.display_name = i[1]
            obj.save()

    def create_organisations(self, counter=None):
        users = get_user_model().objects.all()
        locations = Location.objects.all()

        for i in range(counter):
            number = self.fake.random_digit()
            text = self.fake.text()
            name = self.fake.company()
            org, updated = Organisation.objects.update_or_create(
                name=name,
                location=locations[number],
                organisation_type=number,
                organisation_role=text,
                description=text,
            )
            org.user.add(users[number])

    def create_workshop_sections(self, counter=None):
        for i in range(counter):
            WorkshopSections.objects.update_or_create(
                name=self.fake.sentence())
