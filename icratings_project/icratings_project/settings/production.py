"""Production settings and globals."""


from os import environ

from base import *

import dj_database_url
from memcacheify import memcacheify


# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
	""" Get the environment setting or return exception """
	try:
		return environ[setting]
	except KeyError:
		error_msg = "Set the %s env variable" % setting
		raise ImproperlyConfigured(error_msg)

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = bool(environ.get('DJANGO_DEBUG', ''))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

INSTALLED_APPS += (
    'gunicorn',
    'storages',
)

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {'default': dj_database_url.config()}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = memcacheify()
########## END CACHE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('SECRET_KEY')
########## END SECRET CONFIGURATION

ALLOWED_HOSTS = ['.herokuapp.com', ]

########## S3 STATIC CONFIGURATION
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_setting('AWS_STORAGE_BUCKET_NAME')
STATIC_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
# Used to make sure that only changed files are uploaded with collectstatic
AWS_PRELOAD_METADATA = True
AWS_LOCATION = 'static'
AWS_QUERYSTRING_EXPIRE = 7200
#turns off https for static files (necessary)
AWS_QUERYSTRING_AUTH = False
########## S3 STATIC CONFIGURATION
