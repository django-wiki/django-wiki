from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import settings
from django.contrib.contenttypes.models import ContentType

class NotificationType(models.Model):
    """
    Notification types are added on-the-fly by the
    applications adding new notifications"""
    key = models.CharField(max_length=128, primary_key=True, verbose_name=_(u'unique key'))
    label = models.CharField(max_length=128, verbose_name=_(u'verbose name'),
                             blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    
class Settings(models.Model):
    
    user = models.ForeignKey(User)
    interval = models.SmallIntegerField(choices=settings.INTERVALS, verbose_name=_(u'interval'),
                                        default=settings.INTERVALS_DEFAULT)

class Subscription(models.Model):
    
    settings = models.ForeignKey(Settings)
    notification_type = models.ForeignKey(NotificationType)
    object_id = models.CharField(max_length=64, null=True, blank=True, 
                                 help_text=_(u'Leave this blank to subscribe to any kind of object'))
    send_emails = models.BooleanField(default=True)

class Notification(models.Model):
    
    subscription = models.ForeignKey(Subscription)
    message = models.TextField()
    url = models.URLField(blank=True, null=True, verbose_name=_(u'link for notification'))
    is_viewed = models.BooleanField(default=False)
    is_emailed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def create_notifications(cls, key, **kwargs):
        if not key or not isinstance(key, str):
            raise KeyError('No notification key (string) specified.')
        
        notification_type = NotificationType.objects.get_or_create(key=key)
        
        objects_created = []
        for subscription in Subscription.objects.filter(Q(key=key)|Q(key=None),
                                                        notification_type=notification_type,
                                                        ):
            objects_created.append(
               cls.objects.create(subscription=subscription, **kwargs)
            )
        
        return objects_created
        