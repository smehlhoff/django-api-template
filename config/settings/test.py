from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': 'postgres',
        'PORT': '5432',
    },
}

DEBUG = False

# This will make tests run faster
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

SECRET_KEY = 'jr7)nuw^&47$z@+h7^yd-np22p)8e_2e)i&3y#z8br_ae_yr(c'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
