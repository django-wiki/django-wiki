# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

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

from wiki.conf import settings 

class ArticlePlugin(models.Model):
    """Always extend from this if you're making a plugin. That way, a deletion
    of an article will CASCADE to your plugin, and the database will be kept
    clean. Furthermore, it's possible to list all plugins and maintain generic
    properties in the future..."""    
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, 
                                verbose_name=_(u"article"))
    
    deleted = models.BooleanField(default=False)
    
    def purge(self):
        """Remove related contents completely, ie. media files."""
        pass
    
    class Meta:
        app_label = settings.APP_LABEL
    
class ReusablePlugin(ArticlePlugin):
    """Extend from this model if you have a plugin that may be related to many
    articles. Please note that the ArticlePlugin.article ForeignKey STAYS! This
    is in order to maintain an explicit set of permissions. If you do not like this,
    you can override can_read and can_write."""
    # The article on which the plugin was originally created.
    # Used to apply permissions.
    ArticlePlugin.article.on_delete=models.SET_NULL
    ArticlePlugin.article.verbose_name=_(u'original article')
    ArticlePlugin.article.help_text=_(u'Permissions are inherited from this article')
    ArticlePlugin.article.null = True
    ArticlePlugin.article.blank = True
    
    articles = models.ManyToManyField(Article, related_name='shared_plugins_set')
    
    # Permission methods - you may override these, if they don't fit your logic.
    def can_read(self, *args, **kwargs):
        if self.article:
            return self.article.can_read(*args, **kwargs)
        return False
    
    def can_write(self, *args, **kwargs):
        if self.article:
            return self.article.can_write(*args, **kwargs)
        return False
    
    def save(self, *args, **kwargs):
        
        # Automatically make the original article the first one in the added set
        if not self.article:
            articles = self.articles.all()
            if articles.count() == 0:
                self.article = articles[0]
            
        super(ReusablePlugin, self).save(*args, **kwargs)
    
    class Meta:
        app_label = settings.APP_LABEL

class RevisionPluginCreateError(Exception): pass

class RevisionPlugin(ArticlePlugin):
    """
    Inherit from this model and make sure to specify an article when
    saving a new instance. This way, a new revision will be created, and
    users are able to roll back to the a previous revision (in which your
    plugin wasn't related to the article).
    
    Furthermore, your plugin relation is kept when new revisions are created.
    
    Usage:
    
    class YourPlugin(RevisionPlugin):
        ...
    
    Creating new plugins instances:
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
        app_label = settings.APP_LABEL

######################################################
# SIGNAL HANDLERS
######################################################

# Look at me. I'm a plane.
# And the plane becomes a metaphor for my life.
# It's my art, when I disguise my body in the shape of a plane.
# (Shellac, 1993)

def update_revision_plugins(instance, *args, **kwargs):
    """Every time a new article revision is created, we update all active 
    plugins to match this article revision"""
    if kwargs.get('created', False):
        p_revisions = RevisionPlugin.objects.filter(article=instance.article, deleted=False)
        p_revisions.update(revision=instance)

signals.post_save.connect(update_revision_plugins, ArticleRevision)