# -*- coding: utf-8 -*-
from django.conf.urls import url
from django_notify import views

urlpatterns = [
    url('^json/get/$', views.get_notifications, name='json_get', kwargs={}),
    url('^json/mark-read/$', views.mark_read, name='json_mark_read_base', kwargs={}),
    url('^json/mark-read/(\d+)/$', views.mark_read, name='json_mark_read', kwargs={}),
    url('^goto/(?P<notification_id>\d+)/$', views.goto, name='goto', kwargs={}),
    url('^goto/$', views.goto, name='goto_base', kwargs={}),
]

def get_pattern(app_name="notify", namespace="notify"):
    """Every url resolution takes place as "notify:view_name".
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    return urlpatterns, app_name, namespace