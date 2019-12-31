import boto3
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

client = boto3.client('ssm', region_name='us-west-2')


def parameter_store(key):
    resp = client.get_parameter(Name=key, WithDecryption=True)
    return resp['Parameter']['Value']


SECRET_KEY = parameter_store('/prod/SECRET_KEY')

ALLOWED_HOSTS = parameter_store('/prod/ALLOWED_HOSTS')

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parameter_store('/prod/PSQL_DB_NAME'),
        'USER': parameter_store('/prod/PSQL_USERNAME'),
        'PASSWORD': parameter_store('/prod/PSQL_PASSWORD'),
        'HOST': parameter_store('/prod/PSQL_HOSTNAME'),
        'PORT': parameter_store('/prod/PSQL_PORT'),
    },
}

DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = 300

DEBUG = False

EMAIL_HOST = parameter_store('/prod/EMAIL_HOST')
EMAIL_HOST_USER = parameter_store('/prod/EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = parameter_store('/prod/EMAIL_HOST_PASSWORD')
EMAIL_PORT = parameter_store('/prod/EMAIL_PORT')
EMAIL_USE_TLS = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# https://wiki.mozilla.org/Security/Guidelines/Web_Security#HTTP_Strict_Transport_Security
SECURE_HSTS_SECONDS = 63072000
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'

# Default logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

# Sentry logging
sentry_sdk.init(
    dsn=parameter_store('/prod/SENTRY_DSN'),
    integrations=[DjangoIntegration(), AwsLambdaIntegration()]
)

INSTALLED_APPS += ['storages', ]

AWS_ACCESS_KEY_ID = parameter_store('/prod/AWS_ACCESS_KEY_ID_BUCKET')
AWS_SECRET_ACCESS_KEY = parameter_store('/prod/AWS_SECRET_ACCESS_KEY_BUCKET')
AWS_STORAGE_BUCKET_NAME = parameter_store('/prod/AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False

# https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching#cache-control
# 86400 = (60 seconds x 60 minutes x 24 hours)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'config.storage.MediaStorage'

STATICFILES_LOCATION = 'static'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATICFILES_STORAGE = 'config.storage.StaticStorage'
