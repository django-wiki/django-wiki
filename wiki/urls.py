# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

from wiki.views import article, accounts
from wiki.conf import settings
from wiki.core.plugins import registry

urlpatterns = patterns('',
    url('^$', article.ArticleView.as_view(), name='root', kwargs={'path': ''}),   
    url('^create-root/$', 'wiki.views.article.root_create', name='root_create'),   
    url('^_search/$', article.SearchView.as_view(), name='search'),   
    url('^_revision/diff/(?P<revision_id>\d+)/$', 'wiki.views.article.diff', name='diff'),
)

urlpatterns += patterns('',
    url('^_accounts/sign-up/$', accounts.Signup.as_view(), name='signup'),   
    url('^_accounts/logout/$', accounts.Logout.as_view(), name='logout'),   
    url('^_accounts/login/$', accounts.Login.as_view(), name='login'),   
)

urlpatterns += patterns('',
    # This one doesn't work because it don't know where to redirect after...   
    url('^_revision/change/(?P<article_id>\d+)/(?P<revision_id>\d+)/$', 'wiki.views.article.change_revision', name='change_revision'),   
    url('^_revision/preview/(?P<article_id>\d+)/$', article.Preview.as_view(), name='preview_revision'),   
    url('^_revision/merge/(?P<article_id>\d+)/(?P<revision_id>\d+)/preview/$', 'wiki.views.article.merge', name='merge_revision_preview', kwargs={'preview': True}),   
    
    # Paths decided by article_ids
    url('^(?P<article_id>\d+)/$', article.ArticleView.as_view(), name='get'),   
    url('^(?P<article_id>\d+)/delete/$', article.Delete.as_view(), name='delete'),   
    url('^(?P<article_id>\d+)/deleted/$', article.Deleted.as_view(), name='deleted'),   
    url('^(?P<article_id>\d+)/edit/$', article.Edit.as_view(), name='edit'),   
    url('^(?P<article_id>\d+)/preview/$', article.Preview.as_view(), name='preview'),   
    url('^(?P<article_id>\d+)/history/$', article.History.as_view(), name='history'),   
    url('^(?P<article_id>\d+)/settings/$', article.Settings.as_view(), name='settings'),   
    url('^(?P<article_id>\d+)/source/$', article.Source.as_view(), name='source'),   
    url('^(?P<article_id>\d+)/revision/change/(?P<revision_id>\d+)/$', 'wiki.views.article.change_revision', name='change_revision'),   
    url('^(?P<article_id>\d+)/revision/merge/(?P<revision_id>\d+)/$', 'wiki.views.article.merge', name='merge_revision'),
    url('^(?P<article_id>\d+)/plugin/(?P<slug>\w+)/$', article.Plugin.as_view(), name='plugin'),

)

for plugin in registry.get_plugins().values():
    slug = getattr(plugin, 'slug', None)
    plugin_urlpatterns = getattr(plugin, 'urlpatterns', None)
    if slug and plugin_urlpatterns:
        urlpatterns += patterns('',
            url('^(?P<article_id>\d+)/plugin/'+slug+'/', include(plugin_urlpatterns)),   
            url('^(?P<path>.+/|)_plugin/'+slug+'/', include(plugin_urlpatterns)),   
        )

urlpatterns += patterns('',
    # Paths decided by URLs
    url('^(?P<path>.+/|)_create/$', article.Create.as_view(), name='create'),   
    url('^(?P<path>.+/|)_delete/$', article.Delete.as_view(), name='delete'),   
    url('^(?P<path>.+/|)_deleted/$', article.Deleted.as_view(), name='deleted'),   
    url('^(?P<path>.+/|)_edit/$', article.Edit.as_view(), name='edit'),   
    url('^(?P<path>.+/|)_preview/$', article.Preview.as_view(), name='preview'),   
    url('^(?P<path>.+/|)_history/$', article.History.as_view(), name='history'),   
    url('^(?P<path>.+/|)_dir/$', article.Dir.as_view(), name='dir'),   
    url('^(?P<path>.+/|)_settings/$', article.Settings.as_view(), name='settings'),   
    url('^(?P<path>.+/|)_source/$', article.Source.as_view(), name='source'),   
    url('^(?P<path>.+/|)_revision/change/(?P<revision_id>\d+)/$', 'wiki.views.article.change_revision', name='change_revision'),   
    url('^(?P<path>.+/|)_revision/merge/(?P<revision_id>\d+)/$', 'wiki.views.article.merge', name='merge_revision'),
    url('^(?P<path>.+/|)_plugin/(?P<slug>\w+)/$', article.Plugin.as_view(), name='plugin'),
    url('^(?P<path>.+/|)$', article.ArticleView.as_view(), name='get'),   
)

def get_pattern(app_name="wiki", namespace="wiki"):
    """Every url resolution takes place as "wiki:view_name".
       You should not attempt to have multiple deployments of the wiki in a
       single Django project.
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    return urlpatterns, app_name, namespace
