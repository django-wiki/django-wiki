from django import forms
from django.utils.translation import ugettext as _

from wiki.core.baseplugin import PluginSidebarFormMixin
from wiki.plugins.images import models


class SidebarForm(forms.ModelForm, PluginSidebarFormMixin):
    
    def __init__(self, article, user, *args, **kwargs):
        self.article = article
        self.user = user
        super(SidebarForm, self).__init__(*args, **kwargs)
    
    def get_usermessage(self):
        return _(u"New image %s was successfully uploaded. You can use it by selecting it from the list of available images.") % self.instance.get_filename()
    
    def save(self, *args, **kwargs):
        if not self.instance.id:
            image = models.Image()
            image.article = self.article
            kwargs['commit'] = False
            revision = super(SidebarForm, self).save(*args, **kwargs)
            image.add_revision(self.instance, save=True)
            return revision
        return super(SidebarForm, self).save(*args, **kwargs)
    
    class Meta:
        model = models.ImageRevision
        fields = ('image',)