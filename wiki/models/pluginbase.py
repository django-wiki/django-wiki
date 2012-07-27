from django.db import models
from django.utils.translation import ugettext_lazy as _

"""
There are two kinds of plugin objects:
  1) ArticlePlugin - an object associated with an article. Does not reference
     a Revision.
     
  2) RevisionPlugin - an object associated with a revision. This object
     is automatically referenced to each new revision, and if you create
     a new object, a new revision will be created.
  
  3) ReusablePlugin - a plugin that can be used on many articles. Please note
     that the logics for keeping revisions on such plugins are complicated, so you
     have to implement that on your own.
"""

from article import Article, ArticleRevision

class ArticlePlugin(models.Model):
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, 
                                verbose_name=_(u"article"))
    
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_(u"created"))
    
    class Meta:
        abstract = True

class ReusablePlugin(models.Model):
    
    # The article on which the plugin was originally created.
    # Used to apply permissions.
    original_article = models.ForeignKey(Article, on_delete=models.SET_NULL,
                                         verbose_name=_(u'original article'), null=True, blank=True,
                                         related_name='original_plugin_set',
                                         help_text=_(u'Permissions are inherited from this article'))
    
    articles = models.ManyToManyField(Article)

    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_(u"created"))
    
    # Permission methods - you may override these, if they don't fit your logic.
    def can_read(self, *args, **kwargs):
        if self.original_article:
            return self.original_article.can_read(*args, **kwargs)
        return False
    
    def can_write(self, *args, **kwargs):
        if self.original_article:
            return self.original_article.can_write(*args, **kwargs)
        return False
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        
        # Automatically make the original article the first one in the added set
        if not self.original_article:
            articles = self.articles.all()
            if articles.count() == 0:
                self.original_article = articles[0]
            
        super(ReusablePlugin, self).save(*args, **kwargs)
    
class RevisionPluginCreateError(Exception): pass

class RevisionPlugin(models.Model):
    """
    Inherit from this model and make sure to specify an article when
    saving a new instance. This way, a new revision will be created, and
    users are able to roll back to the a previous revision (containing some
    other instance of your plugin).
    
    Usage:
    
    class YourPlugin(RevisionPlugin):
        ...
    
    Creating new plugins:
    YourPlugin(article=article_instance, ...) or
    YourPlugin.objects.create(article=article_instance, ...)
    
    """
    revision = models.ForeignKey(ArticleRevision, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(RevisionPlugin, self).__init__(*args, **kwargs)
        if not self.id and not 'article' in kwargs:
            raise RevisionPluginCreateError("Keyword argument 'article' expected.")
        self.article = kwargs['article']
        
    def get_logmessage(self):
        return _(u"A plugin was changed")
    
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.article.current_revision:
                raise RevisionPluginCreateError("Article does not have a current_revision set.")
            new_revision = ArticleRevision()
            new_revision.inherit_predecessor(self.article)
            new_revision.automatic_log = self.get_logmessage()
            new_revision.save()
            
            self.revision = new_revision
    
    class Meta:
        abstract = True
    
    def get_editor_media(self, editor):
        if editor == 'markitup':
            pass
        if editor == 'markitup':
            pass

