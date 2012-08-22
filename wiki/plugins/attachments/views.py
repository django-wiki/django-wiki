# -*- coding: utf-8 -*-
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from wiki.core.http import send_file
from wiki.decorators import get_article, response_forbidden
from wiki.plugins.attachments import models, settings, forms
from wiki.views.mixins import ArticleMixin


class AttachmentView(ArticleMixin, FormView):
    
    form_class = forms.AttachmentForm
    template_name="wiki/plugins/attachments/index.html"
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        if article.can_moderate(request.user):
            self.attachments = models.Attachment.objects.filter(articles=article).order_by('current_revision__deleted', 'original_filename')
        else:
            self.attachments = models.Attachment.objects.active().filter(articles=article)
        
        # Fixing some weird transaction issue caused by adding commit_manually to form_valid
        return super(AttachmentView, self).dispatch(request, article, *args, **kwargs)
    
    # WARNING! The below decorator silences other exceptions that may occur!
    @transaction.commit_manually
    def form_valid(self, form):
        if (self.request.user.is_anonymous() and not settings.ANONYMOUS or 
            not self.article.can_write(self.request.user)):
            return response_forbidden(self.request, self.article, self.urlpath)
            
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
            messages.success(self.request, _(u'%s was successfully added.') % attachment_revision.get_filename())
        except models.IllegalFileExtension, e:
            transaction.rollback()
            messages.error(self.request, _(u'Your file could not be saved: %s') % e)
        except Exception:
            transaction.rollback()
            messages.error(self.request, _(u'Your file could not be saved, probably because of a permission error on the web server.'))
        
        transaction.commit()
        return redirect("wiki:attachments_index", path=self.urlpath.path, article_id=self.article.id)
    
    def get_context_data(self, **kwargs):
        kwargs['attachments'] = self.attachments
        kwargs['search_form'] = forms.SearchForm()
        kwargs['selected_tab'] = 'attachments'
        kwargs['anonymous_disallowed'] = self.request.user.is_anonymous() and not settings.ANONYMOUS
        return super(AttachmentView, self).get_context_data(**kwargs)


class AttachmentHistoryView(ArticleMixin, TemplateView):
    
    template_name="wiki/plugins/attachments/history.html"
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        if article.can_moderate(request.user):
            self.attachment = get_object_or_404(models.Attachment, id=attachment_id, articles=article)
        else:
            self.attachment = get_object_or_404(models.Attachment.objects.active(), id=attachment_id, articles=article)
        return super(AttachmentHistoryView, self).dispatch(request, article, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        kwargs['attachment'] = self.attachment
        kwargs['revisions'] = self.attachment.attachmentrevision_set.all().order_by('-revision_number')
        kwargs['selected_tab'] = 'attachments'
        return super(AttachmentHistoryView, self).get_context_data(**kwargs)


class AttachmentReplaceView(ArticleMixin, FormView):
    
    form_class = forms.AttachmentForm
    template_name="wiki/plugins/attachments/replace.html"
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        if self.request.user.is_anonymous() and not settings.ANONYMOUS:
            return response_forbidden(request, article, kwargs.get('urlpath', None))
        if article.can_moderate(request.user):
            self.attachment = get_object_or_404(models.Attachment, id=attachment_id, articles=article)
        else:
            self.attachment = get_object_or_404(models.Attachment.objects.active(), id=attachment_id, articles=article)
        return super(AttachmentReplaceView, self).dispatch(request, article, *args, **kwargs)
    
    def form_valid(self, form):
        
        try:
            attachment_revision = form.save(commit=False)
            attachment_revision.attachment = self.attachment
            attachment_revision.set_from_request(self.request)
            attachment_revision.previous_revision = self.attachment.current_revision
            attachment_revision.save()
            self.attachment.current_revision = attachment_revision
            self.attachment.save()
            messages.success(self.request, _(u'%s uploaded and replaces old attachment.') % attachment_revision.get_filename())
        except models.IllegalFileExtension, e:
            messages.error(self.request, _(u'Your file could not be saved: %s') % e)
            return redirect("wiki:attachments_replace", attachment_id=self.attachment.id,
                            path=self.urlpath.path, article_id=self.article.id)
        except Exception:
            messages.error(self.request, _(u'Your file could not be saved, probably because of a permission error on the web server.'))
            return redirect("wiki:attachments_replace", attachment_id=self.attachment.id,
                            path=self.urlpath.path, article_id=self.article.id)
        
        return redirect("wiki:attachments_index", path=self.urlpath.path, article_id=self.article.id)
    
    def get_form(self, form_class):
        form = FormView.get_form(self, form_class)
        form.fields['file'].help_text = _(u'Your new file will automatically be renamed to match the file already present. Files with different extensions are not allowed.')
        return form
    
    def get_initial(self, **kwargs):
        return {'description': self.attachment.current_revision.description}
    
    def get_context_data(self, **kwargs):
        kwargs['attachment'] = self.attachment
        kwargs['selected_tab'] = 'attachments'
        return super(AttachmentReplaceView, self).get_context_data(**kwargs)

class AttachmentDownloadView(ArticleMixin, View):
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        if article.can_moderate(request.user):
            self.attachment = get_object_or_404(models.Attachment, id=attachment_id, articles=article)
        else:
            self.attachment = get_object_or_404(models.Attachment.objects.active(), id=attachment_id, articles=article)
        revision_id = kwargs.get('revision_id', None)
        if revision_id:
            self.revision = get_object_or_404(models.AttachmentRevision, id=revision_id, attachment__articles=article)
        else:
            self.revision = self.attachment.current_revision
        return super(AttachmentDownloadView, self).dispatch(request, article, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.revision:
            try:
                return send_file(request, self.revision.file.path, 
                                 self.revision.created, self.attachment.original_filename)
            except OSError:
                pass
        raise Http404
    
class AttachmentChangeRevisionView(ArticleMixin, View):
    
    form_class = forms.AttachmentForm
    template_name="wiki/plugins/attachments/replace.html"
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, attachment_id, revision_id, *args, **kwargs):
        if article.can_moderate(request.user):
            self.attachment = get_object_or_404(models.Attachment, id=attachment_id, articles=article)
        else:
            self.attachment = get_object_or_404(models.Attachment.objects.active(), id=attachment_id, articles=article)
        self.revision = get_object_or_404(models.AttachmentRevision, id=revision_id, attachment__articles=article)
        return super(AttachmentChangeRevisionView, self).dispatch(request, article, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.attachment.current_revision = self.revision
        self.attachment.save()
        messages.success(self.request, _(u'Current revision changed for %s.') % self.attachment.original_filename)
        
        return redirect("wiki:attachments_index", path=self.urlpath.path, article_id=self.article.id)
    
    def get_context_data(self, **kwargs):
        kwargs['selected_tab'] = 'attachments'
        return ArticleMixin.get_context_data(self, **kwargs)

class AttachmentAddView(ArticleMixin, View):
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        self.attachment = get_object_or_404(models.Attachment.objects.active().can_write(request.user), id=attachment_id)
        return super(AttachmentAddView, self).dispatch(request, article, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if self.attachment.articles.filter(id=self.article.id):
            self.attachment.articles.add(self.article)
            self.attachment.save()
        messages.success(self.request, _(u'Added a reference to "%(att)s" from "%(art)s".') % 
                         {'att': self.attachment.original_filename,
                          'art': self.article.current_revision.title})        
        return redirect("wiki:attachments_index", path=self.urlpath.path, article_id=self.article.id)
    

class AttachmentDeleteView(ArticleMixin, FormView):
    
    form_class = forms.DeleteForm
    template_name="wiki/plugins/attachments/delete.html"
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        self.attachment = get_object_or_404(models.Attachment, id=attachment_id, articles=article)
        if not self.attachment.can_delete(request.user):
            return response_forbidden(request, article, kwargs.get('urlpath', None))
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
        
        return redirect("wiki:get", path=self.urlpath.path, article_id=self.article.id)

    def get_context_data(self, **kwargs):
        kwargs['attachment'] = self.attachment
        kwargs['selected_tab'] = 'attachments'
        return super(AttachmentDeleteView, self).get_context_data(**kwargs)


class AttachmentSearchView(ArticleMixin, ListView):
    
    template_name="wiki/plugins/attachments/search.html"
    allow_empty = True
    context_object_name = 'attachments'
    paginate_by = 10
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(AttachmentSearchView, self).dispatch(request, article, *args, **kwargs)
    
    def get_queryset(self):
        self.query = self.request.GET.get('query', None)
        if not self.query:
            qs = models.Attachment.objects.get_empty_query_set()
        else:
            qs = models.Attachment.objects.active().can_read(self.request.user)
            qs = qs.filter(Q(original_filename__contains=self.query) |
                           Q(current_revision__description__contains=self.query) |
                           Q(article__current_revision__title__contains=self.query))
        return qs
    
    def get_context_data(self, **kwargs):
        # Is this a bit of a hack? Use better inheritance?
        kwargs_article = ArticleMixin.get_context_data(self, **kwargs)
        kwargs_listview = ListView.get_context_data(self, **kwargs)
        kwargs['search_form'] = forms.SearchForm(self.request.GET)
        kwargs['query'] = self.query
        kwargs.update(kwargs_article)
        kwargs.update(kwargs_listview)
        kwargs['selected_tab'] = 'attachments'
        return kwargs
