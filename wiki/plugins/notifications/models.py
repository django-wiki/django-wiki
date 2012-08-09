# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

from django_notify import notify
from django_notify.models import Subscription

from wiki.plugins.notifications import ARTICLE_CREATE, ARTICLE_EDIT

from wiki import models as wiki_models
from wiki.core import plugins_registry

class ArticleSubscription(wiki_models.pluginbase.ArticlePlugin, Subscription):
    
    def __unicode__(self):
        return (_(u"%(user)s subscribing to %(article)s (%(type)s)") % 
                {'user': self.settings.user.username,
                 'article': self.article.current_revision.title,
                 'type': self.notification_type.label})

def default_url(article):
    try:
        urlpath = wiki_models.URLPath.objects.get(articles=article)
        url = reverse('wiki:get_url', args=(urlpath.path,))
    except wiki_models.URLPath.DoesNotExist:
        url = None
    return url

def post_article_save(instance, **kwargs):
    if kwargs.get('created', False):
        url = default_url(instance)
        notify(_(u'New article created: %s') % instance.title, ARTICLE_CREATE,
               target_object=instance, url=url)

def post_article_revision_save(instance, **kwargs):
    if kwargs.get('created', False):
        url = default_url(instance.article)
        notify(_(u'Article modified: %s') % instance.title, ARTICLE_EDIT,
               target_object=instance.article, url=url)

# Create notifications when new articles are saved. We do NOT care
# about Article objects that are just modified, because many properties
# are modified without any notifications necessary!
signals.post_save.connect(post_article_save, sender=wiki_models.Article,)

# Whenever a new revision is created, we notifý users that an article
# was edited
signals.post_save.connect(post_article_revision_save, sender=wiki_models.ArticleRevision,)

# TODO: We should notify users when the current_revision of an article is
# changed...

##################################################
# NOTIFICATIONS FOR PLUGINS
##################################################
for plugin in plugins_registry.get_plugins():
    
    notifications = getattr(plugin, 'notifications', [])
    for notification_dict in notifications:
        def plugin_notification(instance, **kwargs):
            if kwargs.get('created', False) == notification_dict.get('created', True):
                url = None
                if notification_dict.has_key('get_url'):
                    url = notification_dict['get_url'](instance)
                else:
                    url = default_url(notification_dict['get_article'](instance))
                
                message = notification_dict['message'](instance)
                notify(message, notification_dict['key'],
                       target_object=notification_dict['get_article'](instance), url=url)

        signals.post_save.connect(plugin_notification, sender=notification_dict['model'])
