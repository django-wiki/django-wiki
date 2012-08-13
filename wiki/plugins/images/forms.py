from django import forms

from wiki.plugins import PluginSidebarFormMixin
from wiki.plugins.images import models


class SidebarForm(forms.ModelForm, PluginSidebarFormMixin):
    
    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article')
        super(SidebarForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = models.Image
        fields = ('image',)