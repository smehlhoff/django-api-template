from django.conf import settings
from django.contrib import admin

from .models import User, UserPrimaryEmail, UserProfile, UserActivity

if settings.DEBUG:
    admin.site.register(User)
    admin.site.register(UserPrimaryEmail)
    admin.site.register(UserProfile)
    admin.site.register(UserActivity)
