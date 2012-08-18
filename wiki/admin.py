from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.utils.translation import ugettext_lazy as _
from mptt.admin import MPTTModelAdmin

from django import forms
import models
import editors

class ArticleObjectAdmin(GenericTabularInline):
    model = models.ArticleForObject
    extra = 1
    max_num = 1

class ArticleRevisionForm(forms.ModelForm):
    
    class Meta:
        model = models.ArticleRevision
        
    def __init__(self, *args, **kwargs):
        super(ArticleRevisionForm, self).__init__(*args, **kwargs)
        EditorClass = editors.getEditorClass()
        editor = editors.getEditor()
        self.fields['content'].widget = editor.get_admin_widget()

class ArticleRevisionAdmin(admin.ModelAdmin):
    form = ArticleRevisionForm
    class Media:
        js = editors.getEditorClass().AdminMedia.js
        css = editors.getEditorClass().AdminMedia.css

class ArticleRevisionInline(admin.TabularInline):
    model = models.ArticleRevision
    form = ArticleRevisionForm
    fk_name = 'article'
    extra = 1
    fields = ('content', 'title',  'deleted', 'locked',)
    
    class Media:
        js = editors.getEditorClass().AdminMedia.js
        css = editors.getEditorClass().AdminMedia.css

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
            self.fields['current_revision'].widget = forms.HiddenInput()

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleRevisionInline]
    form = ArticleForm

class URLPathAdmin(MPTTModelAdmin):
    inlines = [ArticleObjectAdmin]
    list_filter = ('site', 'articles__article__current_revision__deleted',
                   'articles__article__created',
                   'articles__article__modified')
    list_display = ('__unicode__', 'article', 'get_created')
    
    def get_created(self, instance):
        return instance.article.created
    get_created.short_description = _(u'created')
    
admin.site.register(models.URLPath, URLPathAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleRevision, ArticleRevisionAdmin)