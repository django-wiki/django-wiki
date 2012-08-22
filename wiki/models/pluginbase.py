# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from wiki.models.article import BaseRevisionMixin

"""
There are three kinds of plugin base models:

  1) SimplePlugin - an object purely associated with an article. Will bump the
     article's revision history upon creation, and rolling back an article will
     make it go away (not from the database, you can roll forwards again).
     
  2) RevisionPlugin - an object with its own revisions. The object will have its
     own history independent of the article. The strategy is that you will provide
     different code for the article text while including it, so it will indirectly
     affect the article history, but you have the force of rolling back this
     object independently.
  
  3) ReusablePlugin - a plugin that can be used on many articles. Please note
     that the logics for keeping revisions on such plugins are complicated, so you
     have to implement that on your own. Furthermore, you need to be aware of
     the permission system!


"""

from article import Article, ArticleRevision

from wiki.conf import settings 

class ArticlePlugin(models.Model):
    """This is the mother of all plugins. Extending from it means a deletion
    of an article will CASCADE to your plugin, and the database will be kept
    clean. Furthermore, it's possible to list all plugins and maintain generic
    properties in the future..."""    
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, 
                                verbose_name=_(u"article"))
    
    deleted = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    
    # Permission methods - you should override these, if they don't fit your logic.
    def can_read(self, **kwargs):
        return self.article.can_read(**kwargs)
    def can_write(self, **kwargs):
        return self.article.can_write(**kwargs)
    def can_delete(self, user):
        return self.article.can_delete(user)
    def can_moderate(self, user):
        return self.article.can_moderate(user)

    def purge(self):
        """Remove related contents completely, ie. media files."""
        pass
    
    class Meta:
        app_label = settings.APP_LABEL
    
class ReusablePlugin(ArticlePlugin):
    """Extend from this model if you have a plugin that may be related to many
    articles. Please note that the ArticlePlugin.article ForeignKey STAYS! This
    is in order to maintain an explicit set of permissions.
    
    In general, it's quite complicated to maintain plugin content that's shared
    between different articles. The best way to go is to avoid this. For inspiration,
    look at wiki.plugins.attachments
    
    You might have to override the permission methods (can_read, can_write etc.)
    if you have certain needs for logic in your reusable plugin.
    """
    # The article on which the plugin was originally created.
    # Used to apply permissions.
    ArticlePlugin.article.on_delete=models.SET_NULL
    ArticlePlugin.article.verbose_name=_(u'original article')
    ArticlePlugin.article.help_text=_(u'Permissions are inherited from this article')
    ArticlePlugin.article.null = True
    ArticlePlugin.article.blank = True
    
    articles = models.ManyToManyField(Article, related_name='shared_plugins_set')
    
    # Since the article relation may be None, we have to check for this
    # before handling permissions....
    def can_read(self, **kwargs):
        return self.article.can_read(**kwargs) if self.article else False
    def can_write(self, **kwargs):
        return self.article.can_write(**kwargs) if self.article else False
    def can_delete(self, user):
        return self.article.can_delete(user) if self.article else False
    def can_moderate(self, user):
        return self.article.can_moderate(user) if self.article else False

    def save(self, *args, **kwargs):
        
        # Automatically make the original article the first one in the added set
        if not self.article:
            articles = self.articles.all()
            if articles.count() == 0:
                self.article = articles[0]
            
        super(ReusablePlugin, self).save(*args, **kwargs)
    
    class Meta:
        app_label = settings.APP_LABEL

class SimplePluginCreateError(Exception): pass

class SimplePlugin(ArticlePlugin):
    """
    Inherit from this model and make sure to specify an article when
    saving a new instance. This way, a new revision will be created, and
    users are able to roll back to the a previous revision (in which your
    plugin wasn't related to the article).
    
    Furthermore, your plugin relation is kept when new revisions are created.
    
    Usage:
    
    class YourPlugin(SimplePlugin):
        ...
    
    Creating new plugins instances:
    YourPlugin(article=article_instance, ...) or
    YourPlugin.objects.create(article=article_instance, ...)
    """
    # The article revision that this plugin is attached to
    article_revision = models.ForeignKey(ArticleRevision, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(SimplePlugin, self).__init__(*args, **kwargs)
        if not self.id and not 'article' in kwargs:
            raise SimplePluginCreateError("Keyword argument 'article' expected.")
            self.article = kwargs['article']
        
    def get_logmessage(self):
        return _(u"A plugin was changed")
    
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.article.current_revision:
                raise SimplePluginCreateError("Article does not have a current_revision set.")
            new_revision = ArticleRevision()
            new_revision.inherit_predecessor(self.article)
            new_revision.automatic_log = self.get_logmessage()
            new_revision.save()
            
            self.article_revision = new_revision
        super(SimplePlugin, self).save(*args, **kwargs)
    
    class Meta:
        app_label = settings.APP_LABEL

class RevisionPlugin(ArticlePlugin):
    """
    If you want your plugin to maintain revisions, extend from this one,
    not SimplePlugin.
    
    This kind of plugin is not attached to article plugins so rolling articles
    back and forth does not affect it.
    """
    # The current revision of this plugin, if any!
    current_revision = models.OneToOneField('RevisionPluginRevision', 
                                            verbose_name=_(u'current revision'),
                                            blank=True, null=True, related_name='plugin_set',
                                            help_text=_(u'The revision being displayed for this plugin.'
                                                         'If you need to do a roll-back, simply change the value of this field.'),
                                            )
    
    def add_revision(self, new_revision, save=True):
        """
        Sets the properties of a revision and ensures its the current
        revision.
        """
        assert self.id or save, ('RevisionPluginRevision.add_revision: Sorry, you cannot add a' 
                                 'revision to a plugin that has not been saved '
                                 'without using save=True')
        if not self.id: self.save()
        revisions = self.revision_set.all()
        try:
            new_revision.revision_number = revisions.latest().revision_number + 1
        except RevisionPluginRevision.DoesNotExist:
            new_revision.revision_number = 0
        new_revision.plugin = self
        new_revision.previous_revision = self.current_revision
        if save: new_revision.save()
        self.current_revision = new_revision
        if save: self.save()

    class Meta:
        app_label = settings.APP_LABEL


class RevisionPluginRevision(BaseRevisionMixin, models.Model):
    """
    If you want your plugin to maintain revisions, make an extra model
    that extends from this one.
    
    (this class is very much copied from wiki.models.article.ArticleRevision
    """
    
    plugin = models.ForeignKey(RevisionPlugin, related_name='revision_set')

    def save(self, *args, **kwargs):
        if (not self.id and
            not self.previous_revision and 
            self.plugin and
            self.plugin.current_revision and 
            self.plugin.current_revision != self):
            
            self.previous_revision = self.plugin.current_revision

        if not self.revision_number:
            try:
                previous_revision = self.plugin.revision_set.latest()
                self.revision_number = previous_revision.revision_number + 1
            except RevisionPluginRevision.DoesNotExist:
                self.revision_number = 1

        super(RevisionPluginRevision, self).save(*args, **kwargs)
        
        if not self.plugin.current_revision:
            # If I'm saved from Django admin, then plugin.current_revision is me!
            self.plugin.current_revision = self
            self.plugin.save()

    class Meta:
        app_label = settings.APP_LABEL
        get_latest_by = ('revision_number',)
        ordering = ('-created',)

######################################################
# SIGNAL HANDLERS
######################################################

# Look at me. I'm a plane.
# And the plane becomes a metaphor for my life.
# It's my art, when I disguise my body in the shape of a plane.
# (Shellac, 1993)

def update_simple_plugins(instance, *args, **kwargs):
    """Every time a new article revision is created, we update all active 
    plugins to match this article revision"""
    if kwargs.get('created', False):
        p_revisions = SimplePlugin.objects.filter(article=instance.article, deleted=False)
        # TODO: This was breaking things. SimplePlugin doesn't have a revision?
        p_revisions.update(article_revision=instance)

signals.post_save.connect(update_simple_plugins, ArticleRevision)