# -*- coding: utf-8 -*-

# Third Party Stuff
import datetime

from django.conf import settings

import factory
from wye.base.constants import OrganisationType, WorkshopLevel, WorkshopStatus


class Factory(factory.DjangoModelFactory):

    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True


class UserTypeFactory(Factory):

    class Meta:
        model = 'profiles.UserType'


class UserFactory(Factory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: 'user%04d' % n)
    email = factory.Sequence(lambda n: 'user%04d@email.com' % n)
    password = factory.PostGeneration(
        lambda obj, *args, **kwargs: obj.set_password('123123'))


class StateFactory(Factory):

    class Meta:
        model = "regions.State"

    name = factory.Sequence(lambda n: "state{}".format(n))


class LocationFactory(Factory):

    class Meta:
        model = "regions.Location"
    name = factory.Sequence(lambda n: "location{}".format(n))
    state = factory.SubFactory("tests.factories.StateFactory")


class OrganisationFactory(Factory):

    class Meta:
        model = "organisations.Organisation"

    name = factory.Sequence(lambda n: "organisation{}".format(n))
    description = factory.Sequence(
        lambda n: "organisation_Description{}".format(n))
    organisation_role = factory.Sequence(
        lambda n: "organisation_role{}".format(n))
    organisation_type = factory.Iterator(dict(OrganisationType.CHOICES).keys())
    location = factory.SubFactory("tests.factories.LocationFactory")


class RegionalLeadFactory(Factory):
    class Meta:
        model = "regions.RegionalLead"

    location = factory.SubFactory("tests.factories.LocationFactory")


class WorkshopSectionFactory(Factory):

    class Meta:
        model = 'workshops.WorkshopSections'


class WorkshopFactory(Factory):

    class Meta:
        model = "workshops.Workshop"

    description = factory.Sequence(
        lambda n: "Workshop_Description{}".format(n))
    no_of_participants = 20
    requester = factory.SubFactory("tests.factories.OrganisationFactory")
    location = factory.SubFactory("tests.factories.LocationFactory")
    workshop_level = factory.Iterator(dict(WorkshopLevel.CHOICES).keys())
    workshop_section = factory.SubFactory(
        "tests.factories.WorkshopSectionFactory")
    status = factory.Iterator(dict(WorkshopStatus.CHOICES).keys())
    expected_date = datetime.datetime.now()


class WorkshopRatingValuesFactory(Factory):

    class Meta:
        model = "workshops.WorkshopRatingValues"
    name = factory.Sequence(lambda n: "Rating{}".format(n))


def create_usertype(**kwargs):
    return UserTypeFactory.create(**kwargs)


def create_user(**kwargs):
    "Create an user along with their dependencies"
    return UserFactory.create(**kwargs)


def create_organisation(**kwargs):
    return OrganisationFactory.create(**kwargs)


def create_regional_lead(**kwargs):
    return RegionalLeadFactory.create(**kwargs)


def create_workshop(**kwargs):
    return WorkshopFactory.create(**kwargs)


def create_workshop_rating(**kwargs):
    return WorkshopRatingValuesFactory.create(**kwargs)


def create_workshop_section(**kwargs):
    return WorkshopSectionFactory.create(**kwargs)


def create_locaiton(**kwargs):
    return LocationFactory.create(**kwargs)

def create_state(**kwargs):
    return StateFactory.create(**kwargs)
