from django.utils.translation import ugettext as _
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.forms.util import flatatt

"""Base classes for different plugin objects.

 * BasePlugin: Create a wiki_plugin.py with a class that inherits from BasePlugin.
 * PluginSidebarFormMixin: Mix in this class in the form that should be rendered in the editor sidebar
 * PluginSettingsFormMixin: ..and this one for a form in the settings tab.

Please have a look in wiki.models.pluginbase to see where to inherit your
plugin's models.
"""

class BasePlugin(object):
    """Plugins should inherit from this"""
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

class BaseEditor():
    """Editors should inherit from this. See wiki.editors for examples."""
    
    # The editor id can be used for conditional testing. If you write your
    # own editor class, you can use the same editor_id as some editor 
    editor_id = 'plaintext'
    media_admin = ()
    media_frontend = ()
    
    def __init__(self, instance=None):
        self.instance = instance
    
    def get_admin_widget(self):
        return forms.Textarea()

    class AdminMedia:
        css = {}
        js = ()

    class Media:
        css = {}
        js = ()


class MarkItUpAdminWidget(forms.Widget):
    """A simplified more fail-safe widget for the backend"""
    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'class': 'markItUp',
                         'rows': '10', 'cols': '40',}
        if attrs:
            default_attrs.update(attrs)
        super(MarkItUpAdminWidget, self).__init__(default_attrs)
    
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))

class MarkItUpWidget(forms.Widget):
    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'class': 'markItUp',
                         'rows': '10', 'cols': '40',}
        if attrs:
            default_attrs.update(attrs)
        super(MarkItUpWidget, self).__init__(default_attrs)
    
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<div><textarea%s>%s</textarea></div>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))

class MarkItUp(BaseEditor):
    editor_id = 'markitup'
    
    def get_admin_widget(self, instance=None):
        return MarkItUpAdminWidget()
    
    def get_widget(self, instance=None):
        return MarkItUpWidget()

    class AdminMedia:
        css = {
            'all': ("wiki/markitup/skins/simple/style.css",
                    "wiki/markitup/sets/admin/style.css",)
        }
        js = ("wiki/markitup/admin.init.js",
              "wiki/markitup/jquery.markitup.js",
              "wiki/markitup/sets/admin/set.js",
              )

    class Media:
        css = {
            'all': ("wiki/markitup/skins/simple/style.css",
                    "wiki/markitup/sets/frontend/style.css",)
        }
        js = ("wiki/markitup/frontend.init.js",
              "wiki/markitup/jquery.markitup.js",
              "wiki/markitup/sets/frontend/set.js",
              )

