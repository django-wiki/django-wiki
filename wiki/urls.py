# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url('^$', 'wiki.views.root', name='root'),   
    url('^create-root/$', 'wiki.views.root_create', name='root_create'),   
    url('(.*)', 'wiki.views.get_url', name='get_url'),   
)

def get_pattern(app_name="wiki", namespace="wiki"):
    """Every url resolution takes place as "wiki:view_name".
       You should not attempt to have multiple deployments of the wiki on
       one site.
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    return urlpatterns, app_name, namespace