from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.translation import ugettext as _


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
    settings_form = None  # A form class to add to the settings tab
    urlpatterns = {
        # General urlpatterns that will reside in /wiki/plugins/plugin-slug/...
        'root': [],
        # urlpatterns that receive article_id or urlpath, i.e.
        # /wiki/ArticleName/plugin/plugin-slug/...
        'article': [],
    }
    article_tab = None  # (_('Attachments'), "fa fa-file")
    article_view = None  # A view for article_id/plugin/slug/
    # A list of notification handlers to be subscribed if the notification
    # system is active
    notifications = []
    # Example
    #        [{'model': models.AttachmentRevision,
    #          'message': lambda obj: _("A file was changed: %s") % obj.get_filename(),
    #          'key': ARTICLE_EDIT,
    #          'created': True,
    #          'get_article': lambda obj: obj.attachment.article}
    #            ]

    markdown_extensions = []

    class RenderMedia:
        js = []
        css = {}


class PluginSidebarFormMixin(forms.ModelForm):

    unsaved_article_title = forms.CharField(widget=forms.HiddenInput(),
                                            required=True)
    unsaved_article_content = forms.CharField(widget=forms.HiddenInput(),
                                              required=False)

    def get_usermessage(self):
        pass


class PluginSettingsFormMixin(object):
    settings_form_headline = _('Settings for plugin')
    settings_order = 1
    settings_write_access = False

    def get_usermessage(self):
        pass
