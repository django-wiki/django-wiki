from __future__ import absolute_import

from django.contrib import admin

from django_notify import models

admin.site.register(models.NotificationType)
admin.site.register(models.Notification)
admin.site.register(models.Settings)
admin.site.register(models.Subscription)
