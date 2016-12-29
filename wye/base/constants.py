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
    _FEEDBACK_PENDING = [5, "FeedBack Pending"]
    _HOLD = [6, "Workshop On Hold"]


@choices
class WorkshopLevel:
    _BEGINNER = [1, "Beginner"]
    _INTERMEDIATE = [2, "Intermediate"]


@choices
class OrganisationType:
    _COLLEGE = [1, "College"]
    _ORGANISATION = [2, "Free Software Organisation"]
    _STUDENT_GROUP = [3, "Student Group"]
    _OTHERS = [4, "Others"]


@choices
class FeedbackType:
    _PRESENTER = [1, "Presenter"]
    _ORGANISATION = [2, "Organisation"]


@choices
class WorkshopRatings:
    _VERY_BAD = [-1, 'Very Bad']
    _BAD = [-2, 'Bad']
    _NEUTRAL = [0, 'Neutral']
    _GOOD = [1, 'Good']
    _VERY_GOOD = [2, 'Very Good']


class WorkshopAction:
    ACTIVE = ('active', 'deactive')
    ASSIGNME = ('opt-in', 'opt-out')


@choices
class ContactFeedbackType:
    _WORKSHOP = [1, "Workshop"]
    _ACCOUNT = [2, "Account"]
    _ORGANISATION = [3, "Organisation"]
    _OTHERS = [4, "Others"]


@choices
class WorkshopAudience:
    _BE_FINAL_YEAR = [1, "B.E Final Year"]
    _BE_THIRD_YEAR = [2, "B.E Third Year"]
    _BE_SECOND_YEAR = [3, "B.E Second Year"]
    _BE_FIRST_YEAR = [4, "B.E Second Year"]
    _MASTER_FINAL_YEAR = [5, "MASTER Final Year"]
    _MASTER_SECOND_YEAR = [6, "MASTER Second Year"]
    _MASTER_FIRST_YEAR = [7, "MASTER Second Year"]
    _TEN_PLUS_TWO = [8, "College 2nd year"]
    _TEN_PLUD_ONE = [9, "College 1 Year"]
    _SCHOOL = [10, "School"]
    _OTHERS = [11, "Others"]
