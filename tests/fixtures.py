# -*- coding: utf-8 -*-
# Standard Library
import functools

# Third Party Stuff
from unittest import mock
import pytest


class PartialMethodCaller:
    def __init__(self, obj, **partial_params):
        self.obj = obj
        self.partial_params = partial_params

    def __getattr__(self, name):
        return functools.partial(
            getattr(self.obj, name), **self.partial_params)


@pytest.fixture
def client():
    '''Overrides default client fixture adding a mocked
    up login method and a json() helper
    '''
    from django.test.client import Client

    class _Client(Client):
        def login(
            self, user=None,
                backend="django.contrib.auth.backends.ModelBackend",
                **credentials):
            if user is None:
                return super(_Client, self).login(**credentials)

            with mock.patch('django.contrib.auth.authenticate') as authenticate:
                user.backend = backend
                authenticate.return_value = user
                return super(_Client, self).login(**credentials)

        @property
        def json(self):
            return PartialMethodCaller(
                obj=self, content_type='application/json;charset="utf-8"')

    return _Client()


@pytest.fixture
def base_url(live_server):
    return live_server.url


@pytest.fixture
def outbox():
    from django.core import mail

    return mail.outbox
