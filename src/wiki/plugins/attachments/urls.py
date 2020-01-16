from django.urls import re_path
from wiki.plugins.attachments import views

urlpatterns = [
    re_path(r"^$", views.AttachmentView.as_view(), name="attachments_index"),
    re_path(
        r"^search/$", views.AttachmentSearchView.as_view(), name="attachments_search"
    ),
    re_path(
        r"^add/(?P<attachment_id>[0-9]+)/$",
        views.AttachmentAddView.as_view(),
        name="attachments_add",
    ),
    re_path(
        r"^replace/(?P<attachment_id>[0-9]+)/$",
        views.AttachmentReplaceView.as_view(),
        name="attachments_replace",
    ),
    re_path(
        r"^history/(?P<attachment_id>[0-9]+)/$",
        views.AttachmentHistoryView.as_view(),
        name="attachments_history",
    ),
    re_path(
        r"^download/(?P<attachment_id>[0-9]+)/$",
        views.AttachmentDownloadView.as_view(),
        name="attachments_download",
    ),
    re_path(
        r"^delete/(?P<attachment_id>[0-9]+)/$",
        views.AttachmentDeleteView.as_view(),
        name="attachments_delete",
    ),
    re_path(
        r"^download/(?P<attachment_id>[0-9]+)/revision/(?P<revision_id>[0-9]+)/$",
        views.AttachmentDownloadView.as_view(),
        name="attachments_download",
    ),
    re_path(
        r"^change/(?P<attachment_id>[0-9]+)/revision/(?P<revision_id>[0-9]+)/$",
        views.AttachmentChangeRevisionView.as_view(),
        name="attachments_revision_change",
    ),
]
