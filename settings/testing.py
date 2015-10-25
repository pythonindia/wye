from .common import *  # noqa

DEBUG = True

SECRET_KEY = 'changeme!!'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "wye",
        'USER': "",
        'PASSWORD': "",
        'HOST': "localhost",
        'PORT': "5432",
    }
}

# E-Mail Settings
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
