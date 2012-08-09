# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext as _

from wiki.core import plugins_registry
from wiki.plugins.attachments import views
from wiki.plugins.attachments import models
from wiki.plugins.attachments import settings
from wiki.plugins.attachments.markdown_extensions import AttachmentExtension
from wiki.plugins.notifications import ARTICLE_EDIT

class AttachmentPlugin(plugins_registry.BasePlugin):
    
    #settings_form = 'wiki.plugins.notifications.forms.SubscriptionForm'
    
    slug = settings.SLUG
    urlpatterns = patterns('',
        url('^$', views.AttachmentView.as_view(), name='attachments_index'),
        url('^search/$', views.AttachmentSearchView.as_view(), name='attachments_search'),
        url('^add/(?P<attachment_id>\d+)/$', views.AttachmentAddView.as_view(), name='attachments_add'),
        url('^replace/(?P<attachment_id>\d+)/$', views.AttachmentReplaceView.as_view(), name='attachments_replace'),
        url('^history/(?P<attachment_id>\d+)/$', views.AttachmentHistoryView.as_view(), name='attachments_history'),
        url('^download/(?P<attachment_id>\d+)/$', views.AttachmentDownloadView.as_view(), name='attachments_download'),
        url('^delete/(?P<attachment_id>\d+)/$', views.AttachmentDeleteView.as_view(), name='attachments_delete'),
        url('^download/(?P<attachment_id>\d+)/revision/(?P<revision_id>\d+)/$', views.AttachmentDownloadView.as_view(), name='attachments_download'),
        url('^change/(?P<attachment_id>\d+)/revision/(?P<revision_id>\d+)/$', views.AttachmentChangeRevisionView.as_view(), name='attachments_revision_change'),
    )
    article_tab = (_(u'Attachments'), "icon-file")
    article_view = views.AttachmentView().dispatch
    article_template_append = 'wiki/plugins/attachments/append.html'
    
    # List of notifications to construct signal handlers for. This
    # is handled inside the notifications plugin.
    notifications = [{'model': models.AttachmentRevision,
                      'message': lambda obj: _(u"A file was changed: %s") % obj.get_filename(),
                      'key': ARTICLE_EDIT,
                      'created': True,
                      'get_article': lambda obj: obj.attachment.article}
                     ]
    
    markdown_extensions = [AttachmentExtension()]
    
    def __init__(self):
        #print "I WAS LOADED!"
        pass
    
plugins_registry.register(AttachmentPlugin)

