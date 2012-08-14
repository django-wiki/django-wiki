from django import forms
from django.utils.translation import ugettext as _

from wiki.plugins import PluginSidebarFormMixin
from wiki.plugins.images import models


class SidebarForm(forms.ModelForm, PluginSidebarFormMixin):
    
    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article')
        super(SidebarForm, self).__init__(*args, **kwargs)
    
    def get_usermessage(self):
        return _(u"New image %s was successfully uploaded. You can use it by selecting it from the list of available images.") % self.instance.get_filename()
    
    class Meta:
        model = models.Image
        fields = ('image',)