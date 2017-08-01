# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Model
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType

from django_notify import settings

_disable_notifications = False

class NotificationType(models.Model):
    """
    Notification types are added on-the-fly by the
    applications adding new notifications"""
    key = models.CharField(max_length=128, primary_key=True, verbose_name=_(u'unique key'),
                           unique=True)
    label = models.CharField(max_length=128, verbose_name=_(u'verbose name'),
                             blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    
    def __unicode__(self):
        return self.key
    
    class Meta:
        app_label = 'django_notify'
        db_table = settings.DB_TABLE_PREFIX + '_notificationtype'
        verbose_name = _(u'type')
        verbose_name_plural = _(u'types')
    
class Settings(models.Model):
    
    user = models.ForeignKey(User)
    interval = models.SmallIntegerField(choices=settings.INTERVALS, verbose_name=_(u'interval'),
                                        default=settings.INTERVALS_DEFAULT)
    
    def __unicode__(self):
        return _(u"Settings for %s") % self.user.username
    
    class Meta:
        app_label = 'django_notify'
        db_table = settings.DB_TABLE_PREFIX + '_settings'
        verbose_name = _(u'settings')
        verbose_name_plural = _(u'settings')

class Subscription(models.Model):
    
    subscription_id = models.AutoField(primary_key=True)
    settings = models.ForeignKey(Settings)
    notification_type = models.ForeignKey(NotificationType)
    object_id = models.CharField(max_length=64, null=True, blank=True, 
                                 help_text=_(u'Leave this blank to subscribe to any kind of object'))
    send_emails = models.BooleanField(default=True)

    def __unicode__(self):
        return _("Subscription for: %s") % str(self.settings.user.username)

    class Meta:
        app_label = 'django_notify'
        db_table = settings.DB_TABLE_PREFIX + '_subscription'
        verbose_name = _(u'subscription')
        verbose_name_plural = _(u'subscriptions')

class Notification(models.Model):
    
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.SET_NULL)
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
        subscriptions.select_related()
        subscriptions.order_by('settings__user')
        prev_user = None
        for subscription in subscriptions:
            # Don't alert the same user several times even though overlapping
            # subscriptions occur.
            if subscription.settings.user == prev_user:
                continue
            objects_created.append(
               cls.objects.create(subscription=subscription, **kwargs)
            )
            prev_user = subscription.settings.user
        
        return objects_created
    
    def __unicode__(self):
        return "%s: %s" % (str(self.subscription.settings.user), self.message)

    class Meta:
        app_label = 'django_notify'
        db_table = settings.DB_TABLE_PREFIX + '_notification'
        verbose_name = _(u'notification')
        verbose_name_plural = _(u'notifications')


def notify(message, key, target_object=None, url=None):
    """
    Notify subscribing users of a new event. Key can be any kind of string,
    just make sure to reuse it where applicable! Object_id is some identifier
    of an object, for instance if a user subscribes to a specific comment thread,
    you could write:

    notify("there was a response to your comment", "comment_response",
           target_object=PostersObject,
           url=reverse('comments:view', args=(PostersObject.id,)))

    The below example notifies everyone subscribing to the "new_comments" key
    with the message "New comment posted".

    notify("New comment posted", "new_comments")

    """

    if _disable_notifications:
        return 0

    if target_object:
        if not isinstance(target_object, Model):
            raise TypeError(_(u"You supplied a target_object that's not an instance of a django Model."))
        object_id = target_object.id
    else:
        object_id = None

    objects = Notification.create_notifications(key, object_id=object_id,
                                                message=message, url=url)
    return len(objects)
