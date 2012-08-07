# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType

from django_notify import settings

class NotificationType(models.Model):
    """
    Notification types are added on-the-fly by the
    applications adding new notifications"""
    key = models.CharField(max_length=128, primary_key=True, verbose_name=_(u'unique key'))
    label = models.CharField(max_length=128, verbose_name=_(u'verbose name'),
                             blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    
    def __unicode__(self):
        return self.key
    
    class Meta:
        db_tablespace = settings.DB_TABLESPACE
        verbose_name = _(u'type')
        verbose_name_plural = _(u'types')
    
class Settings(models.Model):
    
    user = models.ForeignKey(User)
    interval = models.SmallIntegerField(choices=settings.INTERVALS, verbose_name=_(u'interval'),
                                        default=settings.INTERVALS_DEFAULT)
    
    def __unicode__(self):
        return self.user
    
    class Meta:
        db_tablespace = settings.DB_TABLESPACE        
        verbose_name = _(u'settings')
        verbose_name_plural = _(u'settings')

class Subscription(models.Model):
    
    settings = models.ForeignKey(Settings)
    notification_type = models.ForeignKey(NotificationType)
    object_id = models.CharField(max_length=64, null=True, blank=True, 
                                 help_text=_(u'Leave this blank to subscribe to any kind of object'))
    send_emails = models.BooleanField(default=True)

    def __unicode__(self):
        return _("Subscription for: %s") % self.settings.user

    class Meta:
        db_tablespace = settings.DB_TABLESPACE
        verbose_name = _(u'notification type')
        verbose_name_plural = _(u'notification types')

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
        
        object_id = kwargs.pop('object_id', None)
        
        objects_created = []
        subscriptions = Subscription.objects.filter(Q(notification_type__key=key) | 
                                                    Q(notification_type__key=None),)
        if object_id:
            subscriptions = subscriptions.filter(Q(object_id=object_id) |
                                                 Q(object_id=None))
        for subscription in subscriptions:
            objects_created.append(
               cls.objects.create(subscription=subscription, **kwargs)
            )
        
        return objects_created
    
    def __unicode__(self):
        return "%s: %s" % (self.subscription.settings.user, self.message)

    class Meta:
        db_tablespace = settings.DB_TABLESPACE
        verbose_name = _(u'notification')
        verbose_name_plural = _(u'notifications')
