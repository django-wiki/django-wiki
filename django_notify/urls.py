# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url('^json/get/$', 'django_notify.views.get_notifications', name='json_get', kwargs={}),   
    url('^json/mark-read/$', 'django_notify.views.mark_read', name='json_mark_read_base', kwargs={}),   
    url('^json/mark-read/(\d+)/$', 'django_notify.views.mark_read', name='json_mark_read', kwargs={}),   
    url('^goto/(?P<notification_id>\d+)/$', 'django_notify.views.goto', name='goto', kwargs={}),   
    url('^goto/$', 'django_notify.views.goto', name='goto_base', kwargs={}),   
)

def get_pattern(app_name="notify", namespace="notify"):
    """Every url resolution takes place as "notify:view_name".
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    return urlpatterns, app_name, namespace