# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tempfile
import zipfile

from django import forms
from django.core.files.uploadedfile import File
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from wiki.core.permissions import can_moderate
from wiki.plugins.attachments import models
from wiki.plugins.attachments.models import IllegalFileExtension


class AttachmentForm(forms.ModelForm):

    description = forms.CharField(
        label=_('Description'),
        help_text=_('A short summary of what the file contains'),
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article', None)
        self.request = kwargs.pop('request', None)
        self.attachment = kwargs.pop('attachment', None)
        super(AttachmentForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file', None)
        if uploaded_file:
            try:
                models.extension_allowed(uploaded_file.name)
            except IllegalFileExtension as e:
                raise forms.ValidationError(e)
        return uploaded_file

    def save(self, *args, **kwargs):
        commit = kwargs.get('commit', True)
        attachment_revision = super(AttachmentForm, self).save(commit=False)

        # Added because of AttachmentArchiveForm removing file from fields
        # should be more elegant
        attachment_revision.file = self.cleaned_data['file']
        if not self.attachment:
            attachment = models.Attachment()
            attachment.article = self.article
            attachment.original_filename = attachment_revision.get_filename()
            if commit:
                attachment.save()
            attachment.articles.add(self.article)
        else:
            attachment = self.attachment
        attachment_revision.attachment = attachment
        attachment_revision.set_from_request(self.request)
        if commit:
            attachment_revision.save()
        return attachment_revision

    class Meta:
        model = models.AttachmentRevision
        fields = ('file', 'description',)


class AttachmentReplaceForm(AttachmentForm):

    replace = forms.BooleanField(
        label=_('Remove previous'),
        help_text=_('Remove previous attachment revisions and their files (to '
                    'save space)?'),
        required=False,
    )


class AttachmentArchiveForm(AttachmentForm):

    file = forms.FileField(  # @ReservedAssignment
        label=_('File or zip archive'),
        required=True
    )

    unzip_archive = forms.BooleanField(
        label=_('Unzip file'),
        help_text=_(
            'Create individual attachments for files in a .zip file - directories do not work.'),
        required=False)

    def __init__(self, *args, **kwargs):
        super(AttachmentArchiveForm, self).__init__(*args, **kwargs)
        ordered_fields = ['unzip_archive', 'file']
        self.fields.keyOrder = ordered_fields + [k
                                                 for k in self.fields.keys()
                                                 if k not in ordered_fields]

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file', None)
        if uploaded_file and self.cleaned_data.get('unzip_archive', False):
            try:
                self.zipfile = zipfile.ZipFile(uploaded_file.file, mode="r")
                for zipinfo in self.zipfile.filelist:
                    try:
                        models.extension_allowed(zipinfo.filename)
                    except IllegalFileExtension as e:
                        raise forms.ValidationError(e)
            except zipfile.BadZipfile:
                raise forms.ValidationError(ugettext("Not a zip file"))
        else:
            return super(AttachmentArchiveForm, self).clean_file()
        return uploaded_file

    def clean(self):
        super(AttachmentArchiveForm, self).clean()
        if not can_moderate(self.article, self.request.user):
            raise forms.ValidationError(
                ugettext("User not allowed to moderate this article"))
        return self.cleaned_data

    def save(self, *args, **kwargs):

        # This is not having the intended effect
        if 'file' not in self._meta.fields:
            self._meta.fields.append('file')

        if self.cleaned_data['unzip_archive']:
            new_attachments = []
            try:
                for zipinfo in self.zipfile.filelist:
                    f = tempfile.NamedTemporaryFile(mode='r+w')
                    f.write(self.zipfile.read(zipinfo.filename))
                    f = File(f, name=zipinfo.filename)
                    try:
                        attachment = models.Attachment()
                        attachment.article = self.article
                        attachment.original_filename = zipinfo.filename
                        attachment.save()
                        attachment.articles.add(self.article)
                        attachment_revision = models.AttachmentRevision()
                        attachment_revision.file = f
                        attachment_revision.description = self.cleaned_data[
                            'description']
                        attachment_revision.attachment = attachment
                        attachment_revision.set_from_request(self.request)
                        attachment_revision.save()
                        f.close()
                    except models.IllegalFileExtension:
                        raise
                    new_attachments.append(attachment_revision)
            except zipfile.BadZipfile:
                raise
            return new_attachments
        else:
            return super(AttachmentArchiveForm, self).save(*args, **kwargs)

    class Meta(AttachmentForm.Meta):
        fields = ['description', ]


class DeleteForm(forms.Form):

    """This form is both used for dereferencing and deleting attachments"""
    confirm = forms.BooleanField(label=_('Yes I am sure...'),
                                 required=False)

    def clean_confirm(self):
        if not self.cleaned_data['confirm']:
            raise forms.ValidationError(ugettext('You are not sure enough!'))
        return True


class SearchForm(forms.Form):

    query = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'search-query form-control'}),
    )
