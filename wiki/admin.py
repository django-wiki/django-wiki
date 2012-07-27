from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from mptt.admin import MPTTModelAdmin

import models
from django import forms
from django.forms.widgets import HiddenInput

class ArticleObjectAdmin(GenericTabularInline):
    model = models.ArticleForObject
    extra = 1
    max_num = 1

class ArticleForm(forms.ModelForm):

    class Meta:
        model = models.Article

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            revisions = models.ArticleRevision.objects.filter(article=self.instance)
            self.fields['current_revision'].queryset = revisions
        else:
            self.fields['current_revision'].queryset = models.ArticleRevision.objects.get_empty_query_set()
            self.fields['current_revision'].widget = HiddenInput()
            
class ArticleRevisionInline(admin.TabularInline):
    model = models.ArticleRevision
    fk_name = 'article'
    extra = 1
    fields = ('content', 'title', 'user', 'user_message', 'deleted', 'locked', 'redirect')

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleRevisionInline]
    form = ArticleForm

class URLPathAdmin(MPTTModelAdmin):
    inlines = [ArticleObjectAdmin]
    list_filter = ('site', 'articles__article__current_revision__deleted',
                   'articles__article__current_revision__created',
                   'articles__article__modified')
    list_display = ('__unicode__', 'article', 'created')

class ArticleRevisionAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.URLPath, URLPathAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleRevision, ArticleRevisionAdmin)