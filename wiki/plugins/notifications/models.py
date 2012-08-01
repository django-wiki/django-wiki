from django_notify.models import Subscription
from django.utils.translation import ugettext_lazy as _

from wiki.models import pluginbase

class ArticleSubscription(pluginbase.ArticlePlugin, Subscription):
    
    def __unicode__(self):
        return (_(u"%(user)s subscribing to %(article)s (%(type)s)") % 
                {'user': self.user.username,
                 'article': self.article.current_revision.title,
                 'type': self.notification_type.label})
