from __future__ import unicode_literals

from django.contrib import admin

from . import models


class AttachmentRevisionAdmin(admin.TabularInline):
    model = models.AttachmentRevision
    extra = 1
    fields = ('file', 'user', 'user_message')


class AttachmentAdmin(admin.ModelAdmin):

    inlines = [AttachmentRevisionAdmin]


admin.site.register(models.Attachment, AttachmentAdmin)
