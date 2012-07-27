from django.contrib import admin

import models

class ImageAdmin(admin.ModelAdmin):
    
    # Do not let images be added in the admin. An image can only be added
    # from the article admin due to the automatic revision system.
    def has_add_permission(self, request):
        return False

admin.site.register(models.Image, ImageAdmin)