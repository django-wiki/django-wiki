# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from wiki.views import article, accounts
from wiki.conf import settings
from wiki.core.plugins import registry

urlpatterns = [
    url(r'^$', article.ArticleView.as_view(), name='root', kwargs={'path': ''}),
    url(r'^create-root/$', article.root_create, name='root_create'),
    url(r'^_revision/diff/(?P<revision_id>\d+)/$', article.diff, name='diff'),
]

if settings.ACCOUNT_HANDLING:
    urlpatterns += [
        url(r'^_accounts/sign-up/$', accounts.Signup.as_view(), name='signup'),
        url(r'^_accounts/logout/$', accounts.Logout.as_view(), name='logout'),
        url(r'^_accounts/login/$', accounts.Login.as_view(), name='login'),
    ]

urlpatterns += [
    # This one doesn't work because it don't know where to redirect after...   
    url(r'^_revision/change/(?P<article_id>\d+)/(?P<revision_id>\d+)/$', article.change_revision,
        name='change_revision'),
    url(r'^_revision/preview/(?P<article_id>\d+)/$', article.Preview.as_view(), name='preview_revision'),
    url(r'^_revision/merge/(?P<article_id>\d+)/(?P<revision_id>\d+)/preview/$', article.merge,
        name='merge_revision_preview', kwargs={'preview': True}),
    
    # Paths decided by article_ids
    url(r'^(?P<article_id>\d+)/$', article.ArticleView.as_view(), name='get'),
    url(r'^(?P<article_id>\d+)/delete/$', article.Delete.as_view(), name='delete'),
    url(r'^(?P<article_id>\d+)/deleted/$', article.Deleted.as_view(), name='deleted'),
    url(r'^(?P<article_id>\d+)/edit/$', article.Edit.as_view(), name='edit'),
    url(r'^(?P<article_id>\d+)/preview/$', article.Preview.as_view(), name='preview'),
    url(r'^(?P<article_id>\d+)/history/$', article.History.as_view(), name='history'),
    url(r'^(?P<article_id>\d+)/settings/$', article.Settings.as_view(), name='settings'),
    url(r'^(?P<article_id>\d+)/source/$', article.Source.as_view(), name='source'),
    url(r'^(?P<article_id>\d+)/revision/change/(?P<revision_id>\d+)/$', article.change_revision,
        name='change_revision'),
    url(r'^(?P<article_id>\d+)/revision/merge/(?P<revision_id>\d+)/$', article.merge, name='merge_revision'),
    url(r'^(?P<article_id>\d+)/plugin/(?P<slug>\w+)/$', article.Plugin.as_view(), name='plugin'),
]

for plugin in registry.get_plugins().values():
    slug = getattr(plugin, 'slug', None)
    plugin_urlpatterns = getattr(plugin, 'urlpatterns', None)
    if slug and plugin_urlpatterns:
        urlpatterns += [
            url(r'^(?P<article_id>\d+)/plugin/' + slug + '/', include(plugin_urlpatterns)),
            url(r'^(?P<path>.+/|)_plugin/' + slug + '/', include(plugin_urlpatterns)),
        ]

urlpatterns += [
    # Paths decided by URLs
    url(r'^(?P<path>.+/|)_create/$', article.Create.as_view(), name='create'),
    url(r'^(?P<path>.+/|)_delete/$', article.Delete.as_view(), name='delete'),
    url(r'^(?P<path>.+/|)_deleted/$', article.Deleted.as_view(), name='deleted'),
    url(r'^(?P<path>.+/|)_edit/$', article.Edit.as_view(), name='edit'),
    url(r'^(?P<path>.+/|)_preview/$', article.Preview.as_view(), name='preview'),
    url(r'^(?P<path>.+/|)_history/$', article.History.as_view(), name='history'),
    url(r'^(?P<path>.+/|)_dir/$', article.Dir.as_view(), name='dir'),
    url(r'^(?P<path>.+/|)_settings/$', article.Settings.as_view(), name='settings'),
    url(r'^(?P<path>.+/|)_source/$', article.Source.as_view(), name='source'),
    url(r'^(?P<path>.+/|)_revision/change/(?P<revision_id>\d+)/$', article.change_revision, name='change_revision'),
    url(r'^(?P<path>.+/|)_revision/merge/(?P<revision_id>\d+)/$', article.merge, name='merge_revision'),
    url(r'^(?P<path>.+/|)_plugin/(?P<slug>\w+)/$', article.Plugin.as_view(), name='plugin'),
    url(r'^(?P<path>.+/|)$', article.ArticleView.as_view(), name='get'),
]

def get_pattern(app_name="wiki", namespace="wiki"):
    """Every url resolution takes place as "wiki:view_name".
       You should not attempt to have multiple deployments of the wiki in a
       single Django project.
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    return urlpatterns, app_name, namespace