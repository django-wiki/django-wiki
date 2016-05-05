from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin

from . import models


class ImageForm(forms.ModelForm):

    class Meta:
        model = models.Image
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            revisions = models.ImageRevision.objects.filter(
                plugin=self.instance)
            self.fields['current_revision'].queryset = revisions
        else:
            self.fields[
                'current_revision'].queryset = models.ImageRevision.objects.none()
            self.fields['current_revision'].widget = forms.HiddenInput()


class ImageRevisionInline(admin.TabularInline):
    model = models.ImageRevision
    extra = 1
    fields = ('image', 'locked', 'deleted')


class ImageAdmin(admin.ModelAdmin):
    form = ImageForm
    inlines = (ImageRevisionInline,)

admin.site.register(models.Image, ImageAdmin)
