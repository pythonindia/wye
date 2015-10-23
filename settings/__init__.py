# -*- coding: utf-8 -*-
from .common import *  # noqa

try:
    from .dev import *  # noqa
except ImportError:
    pass


# heroku

if 'DYNO' in os.environ:
    from .heroku import *  # noqa
