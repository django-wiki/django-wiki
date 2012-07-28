from django.contrib import admin

import models

class AttachmentRevisionAdmin(admin.TabularInline):
    model = models.AttachmentRevision
    extra = 1
    fields = ('file', 'user', 'user_message')

class AttachmentAdmin(admin.ModelAdmin):
    
    inlines = [AttachmentRevisionAdmin]
    
    # Do not let images be added in the admin. An image can only be added
    # from the article admin due to the automatic revision system.
    #def has_add_permission(self, request):
    #    return False

admin.site.register(models.Attachment, AttachmentAdmin)