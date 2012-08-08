# -*- coding: utf-8 -*-
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.edit import FormView 

from wiki.views.mixins import ArticleMixin
from wiki.decorators import get_article
from wiki.plugins.attachments import forms
from wiki.plugins.attachments import models
from django.contrib import messages
from django.views.generic.base import TemplateView, View
from wiki.core.http import send_file
from django.http import Http404
from django.db import transaction

class AttachmentView(ArticleMixin, FormView):
    
    form_class = forms.AttachmentForm
    template_name="wiki/plugins/attachments/index.html"
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        if request.user.has_perm('wiki.moderator'):
            self.attachments = models.Attachment.objects.filter(articles=article).order_by('current_revision__deleted', 'original_filename')
        else:
            self.attachments = models.Attachment.active_objects.filter(articles=article)
        return super(AttachmentView, self).dispatch(request, article, *args, **kwargs)
    
    @transaction.commit_manually
    def form_valid(self, form):
        
        try:
            attachment_revision = form.save(commit=False)
            attachment = models.Attachment()
            attachment.article = self.article
            attachment.original_filename = attachment_revision.get_filename()
            attachment.save()
            attachment.articles.add(self.article)
            attachment_revision.attachment = attachment
            attachment_revision.set_from_request(self.request)
            attachment_revision.save()
            transaction.commit()
            messages.success(self.request, _(u'%s was successfully added.') % attachment_revision.get_filename())
        except models.IllegalFileExtension, e:
            transaction.rollback()
            messages.error(self.request, _(u'Your file could not be saved: %s') % e)
        
        if self.urlpath:
            return redirect("wiki:attachments_index", self.urlpath.path)
        # TODO: What if no urlpath?        
    
    def get_context_data(self, **kwargs):
        kwargs['attachments'] = self.attachments
        return super(AttachmentView, self).get_context_data(**kwargs)


class AttachmentHistoryView(ArticleMixin, TemplateView):
    
    template_name="wiki/plugins/attachments/history.html"
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        if request.user.has_perm('wiki.moderator'):
            self.attachment = get_object_or_404(models.Attachment, id=attachment_id, articles=article)
        else:
            self.attachment = get_object_or_404(models.Attachment.active_objects, id=attachment_id, articles=article)
        return super(AttachmentHistoryView, self).dispatch(request, article, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        kwargs['attachment'] = self.attachment
        kwargs['revisions'] = self.attachment.attachmentrevision_set.all().order_by('-revision_number')
        return super(AttachmentHistoryView, self).get_context_data(**kwargs)

class AttachmentReplaceView(ArticleMixin, FormView):
    
    form_class = forms.AttachmentForm
    template_name="wiki/plugins/attachments/replace.html"
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        self.attachment = get_object_or_404(models.Attachment.active_objects, id=attachment_id, articles=article)
        return super(AttachmentReplaceView, self).dispatch(request, article, *args, **kwargs)
    
    def form_valid(self, form):
        
        attachment_revision = form.save(commit=False)
        attachment_revision.attachment = self.attachment
        attachment_revision.set_from_request(self.request)
        attachment_revision.previous_revision = self.attachment.current_revision
        attachment_revision.save()
        self.attachment.current_revision = attachment_revision
        self.attachment.save()
        
        messages.success(self.request, _(u'%s uploaded and replaces old attachment.') % attachment_revision.get_filename())
        if self.urlpath:
            return redirect("wiki:attachments_index", self.urlpath.path)
        # TODO: What if we do not have a urlpath?
        
    
    def get_form(self, form_class):
        form = FormView.get_form(self, form_class)
        form.fields['file'].help_text = _(u'Your new file will automatically be renamed to match the file already present. Files with different extensions are not allowed.')
        return form
    
    def get_initial(self, **kwargs):
        return {'description': self.attachment.current_revision.description}
    
    def get_context_data(self, **kwargs):
        kwargs['attachment'] = self.attachment
        return super(AttachmentReplaceView, self).get_context_data(**kwargs)

class AttachmentDownloadView(ArticleMixin, View):
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        self.attachment = get_object_or_404(models.Attachment, id=attachment_id, articles=article)
        revision_id = kwargs.get('revision_id', None)
        if revision_id:
            self.revision = get_object_or_404(models.AttachmentRevision, id=revision_id, attachment__articles=article)
        else:
            self.revision = self.attachment.current_revision
        return super(AttachmentDownloadView, self).dispatch(request, article, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        if self.revision:
            return send_file(request, self.revision.file.path, 
                             self.revision.created, self.attachment.original_filename)
        raise Http404
    
class AttachmentChangeRevisionView(ArticleMixin, View):
    
    form_class = forms.AttachmentForm
    template_name="wiki/plugins/attachments/replace.html"
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, attachment_id, revision_id, *args, **kwargs):
        if request.user.has_perm('wiki.moderator'):
            self.attachment = get_object_or_404(models.Attachment, id=attachment_id, articles=article)
        else:
            self.attachment = get_object_or_404(models.Attachment.active_objects, id=attachment_id, articles=article)
        self.revision = get_object_or_404(models.AttachmentRevision, id=revision_id, attachment__articles=article)
        return super(AttachmentChangeRevisionView, self).dispatch(request, article, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.attachment.current_revision = self.revision
        self.attachment.save()
        messages.success(self.request, _(u'Current revision changed for %s.') % self.attachment.original_filename)
        
        if self.urlpath:
            return redirect("wiki:attachments_index", path=self.urlpath.path)
        # TODO: What if this hasn't got a urlpath.
        else:
            pass


class AttachmentDeleteView(ArticleMixin, FormView):
    
    form_class = forms.DeleteForm
    template_name="wiki/plugins/attachments/delete.html"
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        if request.user.has_perm("wiki.moderator"):
            self.attachment = get_object_or_404(models.Attachment, id=attachment_id, articles=article)
        else:
            self.attachment = get_object_or_404(models.Attachment.active_objects, id=attachment_id, articles=article)
        return super(AttachmentDeleteView, self).dispatch(request, article, *args, **kwargs)
    
    def form_valid(self, form):
        
        if self.attachment.article == self.article:
            revision = models.AttachmentRevision()
            revision.attachment = self.attachment
            revision.set_from_request(self.request)
            revision.deleted = True
            revision.file = self.attachment.current_revision.file if self.attachment.current_revision else None
            revision.description = self.attachment.current_revision.description if self.attachment.current_revision else ""
            revision.save()
            self.attachment.current_revision = revision
            self.attachment.save()
            messages.info(self.request, _(u'The file %s was deleted.') % self.attachment.original_filename)
        else:
            self.attachment.articles.remove(self.article)
            messages.info(self.request, _(u'This article is no longer related to the file %s.') % self.attachment.original_filename)
        
        if self.urlpath:
            return redirect("wiki:get_url", path=self.urlpath.path)
        # TODO: No urlpath?

    def get_context_data(self, **kwargs):
        kwargs['attachment'] = self.attachment
        return super(AttachmentDeleteView, self).get_context_data(**kwargs)
