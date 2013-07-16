# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType

from django_notify import settings

class NotificationType(models.Model):
    """
    Notification types are added on-the-fly by the
    applications adding new notifications
    """
    key = models.CharField(
        max_length=128, 
        primary_key=True, 
        verbose_name=_(u'unique key'),
        unique=True
    )
    label = models.CharField(
        max_length=128, 
        verbose_name=_(u'verbose name'),
        blank=True, 
        null=True
    )
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    
    def __unicode__(self):
        return self.key
    
    class Meta:
        db_table = settings.DB_TABLE_PREFIX + '_notificationtype'
        verbose_name = _(u'type')
        verbose_name_plural = _(u'types')
    
class Settings(models.Model):
    """
    Reusable settings object for a subscription
    """
    
    user = models.ForeignKey(
        settings.USER_MODEL
    )
    interval = models.SmallIntegerField(
        choices=settings.INTERVALS, 
        verbose_name=_(u'interval'),
        default=settings.INTERVALS_DEFAULT
    )
    
    def __unicode__(self):
        obj_name = _(u"Settings for %s") % self.user.username
        return unicode(obj_name)
    
    class Meta:
        db_table = settings.DB_TABLE_PREFIX + '_settings'
        verbose_name = _(u'settings')
        verbose_name_plural = _(u'settings')

class Subscription(models.Model):
    
    settings = models.ForeignKey(Settings)
    notification_type = models.ForeignKey(NotificationType)
    object_id = models.CharField(
        max_length=64, 
        null=True, 
        blank=True, 
        help_text=_(u'Leave this blank to subscribe to any kind of object')
    )
    send_emails = models.BooleanField(default=True)
    latest = models.ForeignKey('Notification', 
        null=True, 
        blank=True, 
        related_name='latest_for'
    )
    
    def __unicode__(self):
        obj_name = _("Subscription for: %s") % str(self.settings.user.username)
        return unicode(obj_name)

    class Meta:
        db_table = settings.DB_TABLE_PREFIX + '_subscription'
        verbose_name = _(u'subscription')
        verbose_name_plural = _(u'subscriptions')

class Notification(models.Model):
    
    subscription = models.ForeignKey(
        Subscription, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    message = models.TextField()
    url = models.CharField(
        verbose_name=_(u'link for notification'),
        blank=True, 
        null=True, 
        max_length=200
    )
    is_viewed = models.BooleanField(default=False)
    is_emailed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    occurrences = models.PositiveIntegerField(
        default=1, 
        verbose_name=_(u'occurrences'),
        help_text=_(
            u'If the same notification was fired multiple '
             'times with no intermediate notifications'
         )
    )
    
    @classmethod
    def create_notifications(cls, key, **kwargs):
        if not key or not isinstance(key, str):
            raise KeyError('No notification key (string) specified.')
        
        object_id = kwargs.pop('object_id', None)
        filter_exclude = kwargs.pop('filter_exclude', {})
        
        objects_created = []
        subscriptions = Subscription.objects.filter(
            Q(notification_type__key=key) | 
            Q(notification_type__key=None),
            **filter_exclude
        )
        if object_id:
            subscriptions = subscriptions.filter(
                Q(object_id=object_id) |
                Q(object_id=None)
            )

        subscriptions = subscriptions.prefetch_related('latest', 'settings')
        subscriptions = subscriptions.order_by('settings__user')
        prev_user = None
        
        for subscription in subscriptions:
            # Don't alert the same user several times even though overlapping
            # subscriptions occur.
            if subscription.settings.user == prev_user:
                continue
            
            # Check if it's the same as the previous message
            latest = subscription.latest
            if latest and (latest.message == kwargs.get('message', None) and 
                latest.url == kwargs.get('url', None) and
                latest.is_viewed == False):
                # Both message and URL are the same, and it hasn't been viewed
                # so just increment occurrence count.
                latest.occurrences = latest.occurrences + 1
                latest.is_emailed = False
                latest.save()
            else:
                # Insert a new notification
                new_obj = cls.objects.create(subscription=subscription, **kwargs)
                objects_created.append(
                   new_obj
                )
                subscription.latest = new_obj
                subscription.save()
            prev_user = subscription.settings.user
        
        return objects_created
    
    def __unicode__(self):
        return "%s: %s" % (str(self.subscription.settings.user), self.message)

    class Meta:
        db_table = settings.DB_TABLE_PREFIX + '_notification'
        verbose_name = _(u'notification')
        verbose_name_plural = _(u'notifications')
        ordering = ('-id',)
