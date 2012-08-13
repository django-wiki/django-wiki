from django.utils.translation import ugettext as _

class BasePlugin(object):
    # Must fill in!
    slug = None
    
    # Optional
    settings_form = None# A form class to add to the settings tab
    urlpatterns = []
    article_tab = None  #(_(u'Attachments'), "icon-file")
    article_view = None # A view for article_id/plugin/slug/
    notifications = []  # A list of notification handlers to be subscribed if the notification system is active
                        # Example
                        #        [{'model': models.AttachmentRevision,
                        #          'message': lambda obj: _(u"A file was changed: %s") % obj.get_filename(),
                        #          'key': ARTICLE_EDIT,
                        #          'created': True,
                        #          'get_article': lambda obj: obj.attachment.article}
                        #            ]

    markdown_extensions = []
    
    pass


class PluginSidebarFormMixin(object):

    def get_usermessage(self):
        pass

class PluginSettingsFormMixin(object):    
    settings_form_headline = _(u'Notifications')
    settings_order = 1
    settings_write_access = False
    
    def get_usermessage(self):
        pass

