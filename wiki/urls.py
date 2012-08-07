# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

from wiki.views import article, accounts
from wiki.conf import settings

urlpatterns = patterns('',
    url('^$', article.ArticleView.as_view(), name='root', kwargs={'path': ''}),   
    url('^create-root/$', 'wiki.views.article.root_create', name='root_create'),   
    url('^_revision/diff/(\d+)/$', 'wiki.views.article.diff', name='diff'),
)

if settings.ACCOUNT_HANDLING:
    urlpatterns += patterns('',
        url('^_accounts/sign-up/$', accounts.Signup.as_view(), name='signup'),   
        url('^_accounts/logout/$', accounts.Logout.as_view(), name='logout'),   
        url('^_accounts/login/$', accounts.Login.as_view(), name='login'),   
    )

urlpatterns += patterns('',
    # This one doesn't work because it don't know where to redirect after...   
    url('^_revision/change/(?P<article_id>\d+)/(?P<revision_id>\d+)/$', 'wiki.views.article.change_revision', name='change_revision'),   
    
    url('^_revision/preview/(?P<article_id>\d+)/$', 'wiki.views.article.preview', name='preview_revision'),   
    url('^_revision/merge/(?P<article_id>\d+)/(?P<revision_id>\d+)/preview/$', 'wiki.views.article.merge', name='merge_revision_preview', kwargs={'preview': True}),   
    url('^(?P<path>.+/|)_create/$', article.Create.as_view(), name='create_url'),   
    url('^(?P<path>.+/|)_edit/$', article.Edit.as_view(), name='edit_url'),   
    url('^(?P<path>.+/|)_preview/$', 'wiki.views.article.preview', name='preview_url'),   
    url('^(?P<path>.+/|)_history/$', article.History.as_view(), name='history_url'),   
    url('^(?P<path>.+/|)_settings/$', article.Settings.as_view(), name='settings_url'),   
    url('^(?P<path>.+/|)_revision/change/(?P<revision_id>\d+)/$', 'wiki.views.article.change_revision', name='change_revision_url'),   
    url('^(?P<path>.+/|)_revision/merge/(?P<revision_id>\d+)/$', 'wiki.views.article.merge', name='merge_revision_url'),   
    url('^(?P<path>.+/|)_plugin/(?P<slug>\w+)/$', article.Plugin.as_view(), name='plugin_url'),   
    url('^(?P<path>.+/|)$', article.ArticleView.as_view(), name='get_url'),   
)

def get_pattern(app_name="wiki", namespace="wiki"):
    """Every url resolution takes place as "wiki:view_name".
       You should not attempt to have multiple deployments of the wiki on
       one site.
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    return urlpatterns, app_name, namespace