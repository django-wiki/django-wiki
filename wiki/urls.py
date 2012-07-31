# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

import views

urlpatterns = patterns('',
    url('^$', 'wiki.views.root', name='root', kwargs={'path': ''}),   
    url('^create-root/$', 'wiki.views.root_create', name='root_create'),   
    url('^_revision/diff/(\d+)/$', 'wiki.views.diff', name='diff'),
    
    # This one doesn't work because it don't know where to redirect after...   
    url('^_revision/change/(?P<article_id>\d+)/(?P<revision_id>\d+)/$', 'wiki.views.change_revision', name='change_revision'),   
    
    url('^_revision/preview/(?P<article_id>\d+)/$', 'wiki.views.preview', name='preview_revision'),   
    url('^_revision/merge/(?P<article_id>\d+)/(?P<revision_id>\d+)/preview/$', 'wiki.views.merge', name='merge_revision_preview', kwargs={'preview': True}),   
    url('^(?P<path>.+/|)_edit/$', 'wiki.views.edit', name='edit_url'),   
    url('^(?P<path>.+/|)_preview/$', 'wiki.views.preview', name='preview_url'),   
    url('^(?P<path>.+/|)_history/$', views.History.as_view(), name='history_url'),   
    url('^(?P<path>.+/|)_revision/change/(?P<revision_id>\d+)/$', 'wiki.views.change_revision', name='change_revision_url'),   
    url('^(?P<path>.+/|)$', 'wiki.views.get_url', name='get_url'),   
)

def get_pattern(app_name="wiki", namespace="wiki"):
    """Every url resolution takes place as "wiki:view_name".
       You should not attempt to have multiple deployments of the wiki on
       one site.
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    return urlpatterns, app_name, namespace