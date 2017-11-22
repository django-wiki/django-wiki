from __future__ import unicode_literals

from django.conf.urls import url
from wiki.plugins.attachments import views

urlpatterns = [
    url(r'^$',
        views.AttachmentView.as_view(),
        name='attachments_index'),
    url(r'^search/$',
        views.AttachmentSearchView.as_view(),
        name='attachments_search'),
    url(r'^add/(?P<attachment_id>[0-9]+)/$',
        views.AttachmentAddView.as_view(),
        name='attachments_add'),
    url(r'^replace/(?P<attachment_id>[0-9]+)/$',
        views.AttachmentReplaceView.as_view(),
        name='attachments_replace'),
    url(r'^history/(?P<attachment_id>[0-9]+)/$',
        views.AttachmentHistoryView.as_view(),
        name='attachments_history'),
    url(r'^download/(?P<attachment_id>[0-9]+)/$',
        views.AttachmentDownloadView.as_view(),
        name='attachments_download'),
    url(r'^delete/(?P<attachment_id>[0-9]+)/$',
        views.AttachmentDeleteView.as_view(),
        name='attachments_delete'),
    url(r'^download/(?P<attachment_id>[0-9]+)/revision/(?P<revision_id>[0-9]+)/$',
        views.AttachmentDownloadView.as_view(),
        name='attachments_download'),
    url(r'^change/(?P<attachment_id>[0-9]+)/revision/(?P<revision_id>[0-9]+)/$',
        views.AttachmentChangeRevisionView.as_view(),
        name='attachments_revision_change'),
]
