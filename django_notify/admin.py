from django.contrib import admin

from django_notify import models
from django_notify import settings

if settings.ENABLE_ADMIN:
    admin.site.register(models.NotificationType)
    admin.site.register(models.Notification)
    admin.site.register(models.Settings)
    admin.site.register(models.Subscription)