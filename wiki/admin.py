from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from mptt.admin import MPTTModelAdmin

import models

class ArticleObjectAdmin(GenericTabularInline):
    model = models.ArticleForObject
    extra = 1
    max_num = 1

class ArticleAdmin(admin.ModelAdmin):
    pass

class URLPathAdmin(MPTTModelAdmin):
    inlines = [ArticleObjectAdmin]
    list_filter = ('site',)
    list_display = ('slug', 'article')

admin.site.register(models.URLPath, URLPathAdmin)
admin.site.register(models.Article, ArticleAdmin)