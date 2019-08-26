# -*- coding: utf-8 -*-
import random
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db import transaction
from allauth.account.models import EmailAddress
from datetime import date
from faker import Faker

from wye.profiles.models import UserType, Profile
from wye.organisations.models import Organisation
from wye.regions.models import Location, State
from wye.workshops.models import WorkshopSections, Workshop
from wye.base.constants import WorkshopStatus, WorkshopLevel


NUMBER_OF_USERS = getattr(settings, "NUMBER_OF_USERS", 10)
NUMBER_OF_LOCATIONS = getattr(settings, "NUMBER_OF_LOCATIONS", 10)
NUMBER_OF_ORGANISATIONS = getattr(settings, "NUMBER_OF_ORGANISATIONS", 10)
NUMBER_OF_WORKSHOP_SECTIONS = getattr(
    settings, "NUMBER_OF_WORKSHOP_SECTIONS", 5)


class Command(BaseCommand):
    help = "Creating Initial demo data for testing application"
    fake = Faker()

    @transaction.atomic
    def handle(self, *args, **options):
        self.fake.seed(4321)

        # Update site url
        self.stdout.write('  Updating domain to localhost:8000')
        site = Site.objects.get_current()
        site.domain, site.name = 'localhost:8000', 'Local'
        site.save()

        # User Type
        self.stdout.write('  Creating User Types')
        self.create_user_type(counter=NUMBER_OF_WORKSHOP_SECTIONS)

        self.stdout.write('  Creating Superuser')
        email = 'admin@pythonexpress.org'
        user = self.create_user(is_superuser=True, username='admin',
                                email=email, is_active=True, is_staff=True,
                                first_name='Admin')

        # User
        self.stdout.write('  Creating sample users')
        for i in range(NUMBER_OF_USERS):
            self.create_user()

        # Location
        self.stdout.write('  Creating sample locations')
        self.create_locations(counter=NUMBER_OF_LOCATIONS)

        # Organization
        self.stdout.write('  Creating sample organisations')
        self.create_organisations(counter=NUMBER_OF_ORGANISATIONS)

        # Workshop
        self.stdout.write('  Creating sample workshop sections')
        self.create_workshop_sections()

        # Profile
        self.stdout.write('  Creating Profile')
        self.create_profile(user)

        # Sample Workshops
        self.stdout.write('  Creating Sample Workshop')
        self.create_sample_workshops(user)
        user_email = EmailAddress.objects.create(
            email=user.email, user=user, verified=True)
        user_email.save()

    def create_user(self, counter=None, **kwargs):
        params = {
            "first_name": kwargs.get('first_name', self.fake.first_name()),
            "last_name": kwargs.get('last_name', self.fake.last_name()),
            "username": kwargs.get('username', self.fake.user_name()),
            "email": kwargs.get('email', self.fake.email()),
            "is_active": kwargs.get('is_active', self.fake.boolean()),
            "is_superuser": kwargs.get('is_superuser', False),
            "is_staff": kwargs.get(
                'is_staff',
                kwargs.get('is_superuser', self.fake.boolean())),
        }

        user, created = get_user_model().objects.get_or_create(**params)

        if params['is_superuser']:
            password = '123123'
            user.set_password(password)
            user.save()

            self.stdout.write(
                "SuperUser created with username: {} and password: {}".format(
                    params['username'], password)
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
            ('poc', 'Organisation Ambassador'),
            ('admin', 'admin'),
            ('volunteer', 'Volunteer'),
            ('student', 'Student')]
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

    def create_workshop_sections(self):
        sections = ["Python2", "Python3", "Django", "Flask", "Gaming"]

        for section in sections:
            self.stdout.write('  Creating %s' % section)
            WorkshopSections.objects.create(name=section)

    def create_profile(self, user):
        django = WorkshopSections.objects.get(name='Django')
        python3 = WorkshopSections.objects.get(name='Python3')
        location = Location.objects.all()[0]
        user_type = UserType.objects.get(slug='admin')
        profile = Profile(
            user=user,
            mobile='8758885872',
            location=location)
        profile.usertype.add(user_type)
        profile.interested_locations.add(location)
        profile.interested_sections.add(django, python3)
        profile.save()
        return profile

    def create_sample_workshops(self, user):
        organisations = Organisation.objects.all()
        # locations = Location.objects.all()
        sections = WorkshopSections.objects.all()

        for i in range(50):
            w = Workshop.objects.create(
                no_of_participants=random.randrange(10, 100),
                expected_date=date(
                    2015, random.randrange(1, 12), random.randrange(1, 29)),
                description=self.fake.text(),
                requester=random.choice(organisations),
                workshop_level=WorkshopLevel.BEGINNER,
                workshop_section=random.choice(sections),
                status=WorkshopStatus.COMPLETED
            )
            w.presenter.add(user)
            w.save()
