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
    _FEEDBACK_PENDING = [5, "FeedBack Pending"]
    _HOLD = [6, "Workshop On Hold"]
    _COMPLETED = [7, "Workshop Completed"]
    _UNABLE_TO_COMPLETE = [8, "Workshop unable to complete"]


@choices
class WorkshopLevel:
    _BEGINNER = [1, "Beginner"]
    _INTERMEDIATE = [2, "Intermediate"]
    _ADVANCE = [2, "Advance"]


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
    _BE_FINAL_YEAR = [1, "Engineering 4th Year"]
    _BE_THIRD_YEAR = [2, "Engineering 3rd Year"]
    _BE_SECOND_YEAR = [3, "Engineering 2ndYear"]
    _BE_FIRST_YEAR = [4, "Engineering 1st Year"]
    _MASTER_FINAL_YEAR = [5, "MCA Final Year"]
    _MASTER_SECOND_YEAR = [6, "MCA Second Year"]
    _MASTER_FIRST_YEAR = [7, "MCA First Year"]
    _DIPLOMA_THIRD_YEAR = [8, "Diploma 3rd Year"]
    _DIPLOMA_SECOND_YEAR = [9, "Diploma 2nd Year"]
    _DIPLOMA_FIRST_YEAR = [10, "Diploma 1st Year"]
    _TEN_PLUS_TWO = [11, "10+2"]
    _TEN_PLUD_ONE = [12, "10+1"]
    _SCHOOL = [13, "School"]
    _OTHERS = [14, "Others"]


@choices
class YesNO:
    _YES = [1, "Yes"]
    _NO = [2, "No"]
