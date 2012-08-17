from django.contrib import admin

import models

class ImageRevisionInline(admin.TabularInline):
    model = models.ImageRevision
    extra = 1
    fields = ('image', 'locked', 'deleted')
    
class ImageAdmin(admin.ModelAdmin):
    inlines = (ImageRevisionInline,)

admin.site.register(models.Image, ImageAdmin)