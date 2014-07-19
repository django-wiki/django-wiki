# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.db import models

from django_nyt.utils import notify
from django_nyt.models import Subscription

from wiki import models as wiki_models
from wiki.models.pluginbase import ArticlePlugin
from wiki.core.plugins import registry
from wiki.plugins.notifications import settings
from wiki.plugins.notifications.util import get_title


class ArticleSubscription(ArticlePlugin):
    
    subscription = models.OneToOneField(Subscription)
    
    def __unicode__(self):
        title = (_("%(user)s subscribing to %(article)s (%(type)s)") %
                 {'user': self.settings.user.username,
                  'article': self.article.current_revision.title,
                  'type': self.notification_type.label})
        return unicode(title)
    
    class Meta:
        unique_together = ('subscription', 'articleplugin_ptr')
        if settings.APP_LABEL:
            app_label = settings.APP_LABEL
    

def default_url(article, urlpath=None):
    if urlpath:
        return reverse('wiki:get', kwargs={'path': urlpath.path})
    return article.get_absolute_url()


def post_article_revision_save(**kwargs):
    instance = kwargs['instance']
    if kwargs.get('created', False):
        url = default_url(instance.article)
        filter_exclude = {'settings__user': instance.user}
        if instance.deleted:
            notify(_('Article deleted: %s') % get_title(instance), settings.ARTICLE_EDIT,
                   target_object=instance.article, url=url, filter_exclude=filter_exclude)
        elif instance.previous_revision:
            notify(_('Article modified: %s') % get_title(instance), settings.ARTICLE_EDIT,
                   target_object=instance.article, url=url, filter_exclude=filter_exclude)
        else:
            notify(_('New article created: %s') % get_title(instance), settings.ARTICLE_EDIT,
                   target_object=instance, url=url, filter_exclude=filter_exclude)
            
# Whenever a new revision is created, we notifý users that an article
# was edited
signals.post_save.connect(post_article_revision_save, sender=wiki_models.ArticleRevision,)

# TODO: We should notify users when the current_revision of an article is
# changed...

##################################################
# NOTIFICATIONS FOR PLUGINS
##################################################
for plugin in registry.get_plugins():
    
    notifications = getattr(plugin, 'notifications', [])
    for notification_dict in notifications:
        def plugin_notification(instance, **kwargs):
            if notification_dict.get('ignore', lambda x: False)(instance):
                return
            if kwargs.get('created', False) == notification_dict.get('created', True):
                url = None
                if 'get_url' in notification_dict:
                    url = notification_dict['get_url'](instance)
                else:
                    url = default_url(notification_dict['get_article'](instance))
                
                message = notification_dict['message'](instance)
                notify(message, notification_dict['key'],
                       target_object=notification_dict['get_article'](instance), url=url)

        signals.post_save.connect(plugin_notification, sender=notification_dict['model'])
