# -*- coding: utf-8 -*-

# Third Party Stuff
from django.conf import settings

import factory
from wye.base.constants import OrganisationType


class Factory(factory.DjangoModelFactory):

    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True


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
    #user = factory.SubFactory("tests.factories.UserFactory")
#
#     @factory.post_generation
#     def user(self, create, extracted, **kwargs):
#         u = UserFactory.create(**kwargs)
#         self.user.add(u)
#         self.save()


def create_user(**kwargs):
    "Create an user along with their dependencies"
    return UserFactory.create(**kwargs)


def create_organisation(**kwargs):
    print('*' * 10)
    print(kwargs)
    print('*' * 10)
    o = OrganisationFactory.create(**kwargs)
    return o
