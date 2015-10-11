# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect


def _user_attributes(cls):
    # gives all inbuilt attrs
    defaults = dir(type(str('defaults'), (object,), {}))
    return [
        item[0] for item in inspect.getmembers(cls) if item[0] not in defaults]


def choices(cls):
    """
    Decorator to set `CHOICES` and other attributes
    """
    _choices = []
    for attr in _user_attributes(cls):
        val = getattr(cls, attr)
        setattr(cls, attr[1:], val[0])
        _choices.append((val[0], val[1]))
    setattr(cls, 'CHOICES', tuple(_choices))
    return cls


@choices
class WorkshopStatus:
    _DRAFT = [1, "Draft"]
    _REQUESTED = [2, "Workshop Requested"]
    _ACCEPTED = [3, "Workshop Accepted "]
    _DECLINED = [4, "Workshop Declined"]
    _COMPLETED = [5, "Workshop Completed"]
    _HOLD = [6, "Workshop On Hold"]
