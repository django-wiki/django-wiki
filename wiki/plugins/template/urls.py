from django.conf.urls import patterns, url

from wiki.plugins.template import views

urlpatterns = patterns('',
    url(r'^$',
        views.TemplateView.as_view(),
        name='template_index'
    ),
    url(r'^create/$',
        views.TemplateCreateView.as_view(),
        name='template_create'
    ),
    url(r'^search/$',
        views.TemplateSearchView.as_view(),
        name='template_search'
    ),
    url(r'^(?P<template_id>\d+)/add/to/article/$',
        views.TemplateAddView.as_view(),
        name='template_add_to_article'
    ),
    url(r'^history/(?P<template_id>\d+)/$',
        views.TemplateHistoryView.as_view(),
        name='template_history'
    ),
    url(r'^delete/(?P<template_id>\d+)/$',
       views.TemplateDeleteView.as_view(),
       name='template_delete'
    ),
    url(r'^change/(?P<template_id>\d+)/revision/(?P<revision_id>\d+)/$',
       views.TemplateChangeRevisionView.as_view(),
       name='template_revision_change'
    ),
    url(r'^json/query-title/$',
        views.QueryTitle.as_view(),
        name='template_query_title'
    ),
    url('^(?P<template_id>\d+)/revision/add/$',
        views.RevisionAddView.as_view(),
        name='template_add_revision'
    ),
    url('^(?P<template_id>\d+)/revision/add/preview/$',
        views.EditPreview.as_view(),
        name='template_add_revision_preview'
    ),
    url('^create/preview/$',
        views.CreatePreview.as_view(),
        name='template_create_preview'
    ),
)
