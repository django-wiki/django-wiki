from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin

from . import models


class InputForm(forms.ModelForm):
    class Meta:
        model = models.Input
        exclude = ()


class InputAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article', 'owner', 'key', 'created')
    form = InputForm


admin.site.register(models.Input, InputAdmin)
