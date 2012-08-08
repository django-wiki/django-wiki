# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

from django_notify import notify
from django_notify.models import Subscription

from wiki.plugins.notifications import ARTICLE_CREATE, ARTICLE_EDIT

from wiki import models as wiki_models

class ArticleSubscription(wiki_models.pluginbase.ArticlePlugin, Subscription):
    
    def __unicode__(self):
        return (_(u"%(user)s subscribing to %(article)s (%(type)s)") % 
                {'user': self.settings.user.username,
                 'article': self.article.current_revision.title,
                 'type': self.notification_type.label})

def post_article_save(instance, **kwargs):
    if kwargs.get('created', True):
        urlpath = wiki_models.URLPath.objects.filter(articles=instance)
        if urlpath:
            url = reverse('wiki:get_url', urlpath.path)
        else:
            url = None
        notify(_(u'New article created: %s') % instance.title, ARTICLE_CREATE,
               target_object=instance, url=url)

def post_article_revision_save(instance, **kwargs):
    if kwargs.get('created', False):
        try:
            urlpath = wiki_models.URLPath.objects.get(articles=instance.article)
            url = reverse('wiki:get_url', args=(urlpath.path,))
        except wiki_models.URLPath.DoesNotExist:
            url = None
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

