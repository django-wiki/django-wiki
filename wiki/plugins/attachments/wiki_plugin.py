from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from wiki.core import plugins_registry
from wiki.views.mixins import ArticleMixin
from wiki.decorators import get_article

class AttachmentView(ArticleMixin, TemplateView):

    template_name="wiki/plugins/attachments/tab.html"
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(AttachmentView, self).dispatch(request, article, *args, **kwargs)
    
    
class AttachmentPlugin(plugins_registry.BasePlugin):
    
    #settings_form = 'wiki.plugins.notifications.forms.SubscriptionForm'
    
    slug = 'attachments'
    article_tab = (_(u'Attachments'), "icon-file")
    article_view = AttachmentView().dispatch
    article_template_append = 'wiki/plugins/attachments/append.html'
    
    def __init__(self):
        #print "I WAS LOADED!"
        pass
    
plugins_registry.register(AttachmentPlugin)

