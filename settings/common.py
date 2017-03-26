"""
Django settings for wye project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from celery.schedules import crontab
import datetime
import djcelery
import os
from os.path import join


ADMINS = (
    ('Vijay', 'vnbang2003@gmail.com'),
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = join(BASE_DIR, 'wye')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(7a-1a$5rsmii8grbapha!r4du4dmh1xnp0p8_(lnx_cx(p7+^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

SITE_ID = 1
# Application definition

# General project information
# These are available in the template as SITE_INFO.<title>
SITE_VARIABLES = {
    'site_name': os.environ.get('SITE_NAME', 'PythonExpress'),
    'site_description': '',
    'footer': {
        'copyright': {
            'year': '2014-{}'.format(datetime.datetime.today().strftime('%Y')),
            'url': 'http://pssi.org.in/',
            'label': 'Python Software Society of India'
        },
        'social': [
            {
                'media': 'mail',
                'icon': 'fa fa-envelope',
                'label': 'Mailing List',
                'url': 'http://lists.pssi.org.in/cgi-bin/mailman/listinfo/pythonexpress'
            },
            {
                'media': 'github',
                'icon': 'fa fa-github',
                'label': 'Github',
                'url': 'https://github.com/pythonindia/wye'
            },
            {
                'media': 'twitter',
                'icon': 'fa fa-twitter',
                'label': 'Twitter',
                'url': 'https://twitter.com/pythonexpress/'
            },
            {
                'media': 'facebook',
                'icon': 'fa fa-facebook',
                'label': 'Facebook',
                'url': 'https://www.facebook.com/PythonExpressdotin/'
            }
        ]
    }
}

DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

OUR_APPS = (
    'wye.base',
    'wye.profiles',
    'wye.organisations',
    'wye.workshops',
    'wye.regions',
    'wye.social',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'djcelery'
)

INSTALLED_APPS = DEFAULT_APPS + OUR_APPS + THIRD_PARTY_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'wye.urls'
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APP_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.core.context_processors.request',
                'wye.base.context_processors.site_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'wye.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}

ATOMIC_REQUESTS = True

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
TIME_ZONE = 'Asia/Kolkata'
LANGUAGE_CODE = "en"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(APP_DIR, 'assets', 'collected-static')

STATICFILES_DIRS = (
    os.path.join(APP_DIR, 'static'),
)

# Media
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(APP_DIR, 'media')

SITE_PROTOCOL = 'http'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
}

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URLNAME = 'dashboard'
ALLOWED_DATE_FORMAT = (
    '%d-%m-%Y', '%d/%m/%Y',
    '%d/%m/%y')

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATIONA = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[{}] ".format(SITE_VARIABLES['site_name'])
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_SIGNUP_FORM_CLASS = 'wye.profiles.forms.SignupForm'

EMAIL_SUBJECT_PREFIX = ACCOUNT_EMAIL_SUBJECT_PREFIX

# E-Mail Settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', ''),
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', ''),
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = SITE_VARIABLES['site_name'] + ' <noreply@pssi.org.in>'

# Social media keys

# Twitter
TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY", "")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET", "")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")

# Google
GOOGLE_MAP_API = os.environ.get("GOOGLE_MAP_API", "")


# Celery
djcelery.setup_loader()

BROKER_URL = 'redis://localhost:6379/0'
CELERY_IMPORTS = ('wye.workshops.tasks',)

CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'send-details-daily': {
        'task': 'wye.workshops.tasks.workshop_reminder',
        'schedule': crontab(hour=7, minute=30),
    },
    'send-upcoming_event_reminder': {
        'task': 'wye.workshops.tasks.workshop_reminder',
        'schedule': crontab(hour=7, minute=30),
        'args': (2, False, False)
    },
    'send-feedback-reminder': {
        'task': 'wye.workshops.tasks.workshop_reminder',
        'schedule': crontab(hour=7, minute=30),
        'args': (2, False, True)
    },
    'send-feedback-second-reminder': {
        'task': 'wye.workshops.tasks.workshop_reminder',
        'schedule': crontab(hour=7, minute=30),
        'args': (2, False, True)
    },
}

CELERY_ACCEPT_CONTENT = ['json']
