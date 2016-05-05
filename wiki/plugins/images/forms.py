from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from wiki.core.plugins.base import PluginSidebarFormMixin
from wiki.plugins.images import models


class SidebarForm(PluginSidebarFormMixin):

    def __init__(self, article, request, *args, **kwargs):
        self.article = article
        self.request = request
        super(SidebarForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True

    def get_usermessage(self):
        return ugettext(
            "New image %s was successfully uploaded. You can use it by selecting it from the list of available images.") % self.instance.get_filename()

    def save(self, *args, **kwargs):
        if not self.instance.id:
            image = models.Image()
            image.article = self.article
            kwargs['commit'] = False
            revision = super(SidebarForm, self).save(*args, **kwargs)
            revision.set_from_request(self.request)
            image.add_revision(self.instance, save=True)
            return revision
        return super(SidebarForm, self).save(*args, **kwargs)

    class Meta:
        model = models.ImageRevision
        fields = ('image',)


class RevisionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.image = kwargs.pop('image')
        self.request = kwargs.pop('request')
        super(RevisionForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True

    def save(self, *args, **kwargs):
        if not self.instance.id:
            kwargs['commit'] = False
            revision = super(RevisionForm, self).save(*args, **kwargs)
            revision.inherit_predecessor(self.image, skip_image_file=True)
            revision.deleted = False  # Restore automatically if deleted
            revision.set_from_request(self.request)
            self.image.add_revision(self.instance, save=True)
            return revision
        return super(RevisionForm, self).save(*args, **kwargs)

    class Meta:
        model = models.ImageRevision
        fields = ('image',)


class PurgeForm(forms.Form):

    confirm = forms.BooleanField(label=_('Are you sure?'), required=False)

    def clean_confirm(self):
        confirm = self.cleaned_data['confirm']
        if not confirm:
            raise forms.ValidationError(ugettext('You are not sure enough!'))
        return confirm
