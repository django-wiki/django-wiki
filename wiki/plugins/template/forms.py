# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext as _

from wiki.editors import getEditor
from wiki.plugins.template import models


class TemplateForm(forms.ModelForm):

    template_title = forms.SlugField(
        label=_('Template title'),
        required=True,
        help_text=_(
            'Use only alphanumeric characters and - or _. '
            'Note that you cannot change the title after creating the template.'
        ),
    )
    extend_to_children = forms.BooleanField(
        label=_('Extend'),
        help_text=_(
            'You can extent this template to children articles.'
            'They will be able to use this template without import.'
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article', None)
        self.request = kwargs.pop('request', None)
        self.template = kwargs.pop('template', None)
        super(TemplateForm, self).__init__(*args, **kwargs)
        if self.template and self.template.extend_to_children:
            self.fields["extend_to_children"].widget.attrs[
                "checked"] = "checked"

    def clean_template_title(self):
        title = self.cleaned_data['template_title']
        if self.template and self.template.template_title:
            return self.template.template_title
        if models.Template.objects.filter(template_title=title):
            raise forms.ValidationError(
                _('A template named "%s" already exists.') % title
            )
        return title

    def save(self, *args, **kwargs):
        commit = kwargs.get('commit', True)
        template_revision = super(TemplateForm, self).save(commit=False)

        if not self.template:
            template = models.Template()
            template.article = self.article
            template.template_title = self.cleaned_data['template_title']
            template.extend_to_children = self.cleaned_data[
                'extend_to_children']
            if commit:
                template.save()
            template.articles.add(self.article)
        else:
            template = self.template
        template_revision.template = template
        template_revision.set_from_request(self.request)
        if commit:
            template_revision.save()
        return template_revision

    class Meta:
        model = models.TemplateRevision
        fields = (
            'template_title',
            'template_content',
            'extend_to_children',
            'description',
        )
        widgets = {
            'template_content': getEditor().get_widget(),
            'description': forms.TextInput(),
        }


class RevisionForm(forms.ModelForm):

    extend_to_children = forms.BooleanField(
        label=_('Extend'),
        help_text=_(
            'You can extent this template to children articles.'
            'They will be able to use this template without import.'
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.template = kwargs.pop('template')
        super(RevisionForm, self).__init__(*args, **kwargs)
        if self.template and self.template.extend_to_children:
            self.fields["extend_to_children"].widget.attrs[
                "checked"] = "checked"

    def save(self, *args, **kwargs):
        template_revision = super(RevisionForm, self).save(commit=False)
        template = self.template
        template_revision.template = template
        template_revision.set_from_request(self.request)
        template_revision.save()
        template.current_revision = template_revision
        template.extend_to_children = self.cleaned_data['extend_to_children']
        template.save()
        return template_revision

    class Meta:
        model = models.TemplateRevision
        fields = ('template_content', 'description', 'extend_to_children')
        widgets = {
            'template_content': getEditor().get_widget(),
            'description': forms.TextInput(),
        }


class DeleteForm(forms.Form):

    """This form is both used for dereferencing and deleting template"""
    confirm = forms.BooleanField(label=_('Yes I am sure...'),
                                 required=False)

    def clean_confirm(self):
        if not self.cleaned_data['confirm']:
            raise forms.ValidationError(_('You are not sure enough!'))
        return True


class SearchForm(forms.Form):

    query = forms.CharField(
        label="", widget=forms.TextInput(attrs={'class': 'search-query'}),)
