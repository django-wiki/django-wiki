# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from wiki.core.http import send_file
from wiki.core.paginator import WikiPaginator
from wiki.decorators import get_article, response_forbidden
from wiki.plugins.attachments import forms, models, settings
from wiki.views.mixins import ArticleMixin


class AttachmentView(ArticleMixin, FormView):

    form_class = forms.AttachmentForm
    template_name = "wiki/plugins/attachments/index.html"

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        if article.can_moderate(request.user):
            self.attachments = models.Attachment.objects.filter(
                articles=article, current_revision__deleted=False
            ).exclude(
                current_revision__file=None
            ).order_by('original_filename')

            self.form_class = forms.AttachmentArchiveForm
        else:
            self.attachments = models.Attachment.objects.active().filter(
                articles=article)

        # Fixing some weird transaction issue caused by adding commit_manually
        # to form_valid
        return super(AttachmentView, self).dispatch(request, article, *args, **kwargs)

    def form_valid(self, form):

        if (self.request.user.is_anonymous() and not settings.ANONYMOUS or
                not self.article.can_write(self.request.user) or
                self.article.current_revision.locked):
            return response_forbidden(self.request, self.article, self.urlpath)

        attachment_revision = form.save()
        if isinstance(attachment_revision, list):
            messages.success(
                self.request, _('Successfully added: %s') %
                (", ".join(
                    [ar.get_filename() for ar in attachment_revision])))
        else:
            messages.success(
                self.request,
                _('%s was successfully added.') %
                attachment_revision.get_filename())
        self.article.clear_cache()

        return redirect(
            "wiki:attachments_index",
            path=self.urlpath.path,
            article_id=self.article.id)

    def get_form_kwargs(self):
        kwargs = super(AttachmentView, self).get_form_kwargs()
        kwargs['article'] = self.article
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        # Needed since Django 1.9 because get_context_data is no longer called
        # with the form instance
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['attachments'] = self.attachments
        kwargs['deleted_attachments'] = models.Attachment.objects.filter(
            articles=self.article,
            current_revision__deleted=True)
        kwargs['search_form'] = forms.SearchForm()
        kwargs['selected_tab'] = 'attachments'
        kwargs['anonymous_disallowed'] = self.request.user.is_anonymous() and not settings.ANONYMOUS
        return super(AttachmentView, self).get_context_data(**kwargs)


class AttachmentHistoryView(ArticleMixin, TemplateView):

    template_name = "wiki/plugins/attachments/history.html"

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        if article.can_moderate(request.user):
            self.attachment = get_object_or_404(
                models.Attachment,
                id=attachment_id,
                articles=article)
        else:
            self.attachment = get_object_or_404(
                models.Attachment.objects.active(),
                id=attachment_id,
                articles=article)
        return super(AttachmentHistoryView, self).dispatch(request, article, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['attachment'] = self.attachment
        kwargs['revisions'] = self.attachment.attachmentrevision_set.all().order_by(
            '-revision_number')
        kwargs['selected_tab'] = 'attachments'
        return super(AttachmentHistoryView, self).get_context_data(**kwargs)


class AttachmentReplaceView(ArticleMixin, FormView):

    form_class = forms.AttachmentForm
    template_name = "wiki/plugins/attachments/replace.html"

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        if request.user.is_anonymous() and not settings.ANONYMOUS:
            return response_forbidden(request, article, kwargs.get('urlpath', None))
        if article.can_moderate(request.user):
            self.attachment = get_object_or_404(
                models.Attachment,
                id=attachment_id,
                articles=article)
            self.can_moderate = True
        else:
            self.attachment = get_object_or_404(
                models.Attachment.objects.active(),
                id=attachment_id,
                articles=article)
            self.can_moderate = False
        return super(AttachmentReplaceView, self).dispatch(request, article, *args, **kwargs)

    def get_form_class(self):
        if self.can_moderate:
            return forms.AttachmentReplaceForm
        else:
            return forms.AttachmentForm

    def form_valid(self, form):

        try:
            attachment_revision = form.save(commit=True)
            attachment_revision.set_from_request(self.request)
            attachment_revision.previous_revision = self.attachment.current_revision
            attachment_revision.save()
            self.attachment.current_revision = attachment_revision
            self.attachment.save()
            messages.success(
                self.request,
                _('%s uploaded and replaces old attachment.') %
                attachment_revision.get_filename())
            self.article.clear_cache()
        except models.IllegalFileExtension as e:
            messages.error(self.request, _('Your file could not be saved: %s') % e)
            return redirect(
                "wiki:attachments_replace",
                attachment_id=self.attachment.id,
                path=self.urlpath.path,
                article_id=self.article.id)

        if self.can_moderate:
            if form.cleaned_data['replace']:
                # form has no cleaned_data field unless self.can_moderate is True
                try:
                    most_recent_revision = self.attachment.attachmentrevision_set.exclude(
                        id=attachment_revision.id,
                        created__lte=attachment_revision.created).latest()
                    most_recent_revision.delete()
                except ObjectDoesNotExist:
                    msg = "{attachment} does not contain any revisions.".format(
                        attachment=str(self.attachment.original_filename)
                    )
                    messages.error(self.request, msg)

        return redirect(
            "wiki:attachments_index",
            path=self.urlpath.path,
            article_id=self.article.id)

    def get_form(self, form_class=None):
        form = super(AttachmentReplaceView, self).get_form(form_class=form_class)
        form.fields['file'].help_text = _(
            'Your new file will automatically be renamed to match the file already present. Files with different extensions are not allowed.')
        return form

    def get_form_kwargs(self):
        kwargs = super(AttachmentReplaceView, self).get_form_kwargs()
        kwargs['article'] = self.article
        kwargs['request'] = self.request
        kwargs['attachment'] = self.attachment
        return kwargs

    def get_initial(self, **kwargs):
        return {'description': self.attachment.current_revision.description}

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['attachment'] = self.attachment
        kwargs['selected_tab'] = 'attachments'
        return super(AttachmentReplaceView, self).get_context_data(**kwargs)


class AttachmentDownloadView(ArticleMixin, View):

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        if article.can_moderate(request.user):
            self.attachment = get_object_or_404(
                models.Attachment,
                id=attachment_id,
                articles=article)
        else:
            self.attachment = get_object_or_404(
                models.Attachment.objects.active(),
                id=attachment_id,
                articles=article)
        revision_id = kwargs.get('revision_id', None)
        if revision_id:
            self.revision = get_object_or_404(
                models.AttachmentRevision,
                id=revision_id,
                attachment__articles=article)
        else:
            self.revision = self.attachment.current_revision
        return super(AttachmentDownloadView, self).dispatch(request, article, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.revision:
            if settings.USE_LOCAL_PATH:
                try:
                    return send_file(
                        request,
                        self.revision.file.path,
                        self.revision.created,
                        self.attachment.original_filename)
                except OSError:
                    pass
            else:
                return HttpResponseRedirect(self.revision.file.url)
        raise Http404


class AttachmentChangeRevisionView(ArticleMixin, View):

    form_class = forms.AttachmentForm
    template_name = "wiki/plugins/attachments/replace.html"

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, attachment_id, revision_id, *args, **kwargs):
        if article.can_moderate(request.user):
            self.attachment = get_object_or_404(
                models.Attachment,
                id=attachment_id,
                articles=article)
        else:
            self.attachment = get_object_or_404(
                models.Attachment.objects.active(),
                id=attachment_id,
                articles=article)
        self.revision = get_object_or_404(
            models.AttachmentRevision,
            id=revision_id,
            attachment__articles=article)
        return super(AttachmentChangeRevisionView, self).dispatch(request, article, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.attachment.current_revision = self.revision
        self.attachment.save()
        self.article.clear_cache()
        messages.success(
            self.request,
            _('Current revision changed for %s.') %
            self.attachment.original_filename)

        return redirect(
            "wiki:attachments_index",
            path=self.urlpath.path,
            article_id=self.article.id)

    def get_context_data(self, **kwargs):
        kwargs['selected_tab'] = 'attachments'
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return ArticleMixin.get_context_data(self, **kwargs)


class AttachmentAddView(ArticleMixin, View):

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, attachment_id, *args, **kwargs):
        self.attachment = get_object_or_404(
            models.Attachment.objects.active().can_write(
                request.user),
            id=attachment_id)
        return super(AttachmentAddView, self).dispatch(request, article, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.attachment.articles.filter(id=self.article.id):
            self.attachment.articles.add(self.article)
            self.attachment.save()
            self.article.clear_cache()
            messages.success(
                self.request,
                _('Added a reference to "%(att)s" from "%(art)s".') % {
                    'att': self.attachment.original_filename,
                    'art': self.article.current_revision.title})
        else:
            messages.error(
                self.request, _('"%(att)s" is already referenced.') %
                {'att': self.attachment.original_filename})
        return redirect(
            "wiki:attachments_index",
            path=self.urlpath.path,
            article_id=self.article.id)


class AttachmentDeleteView(ArticleMixin, FormView):

    form_class = forms.DeleteForm
    template_name = "wiki/plugins/attachments/delete.html"

    @method_decorator(get_article(can_write=True, not_locked=True))
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
            self.article.clear_cache()
            messages.info(self.request, _('The file %s was deleted.') % self.attachment.original_filename)
        else:
            self.attachment.articles.remove(self.article)
            messages.info(
                self.request,
                _('This article is no longer related to the file %s.') %
                self.attachment.original_filename)
        self.article.clear_cache()
        return redirect("wiki:get", path=self.urlpath.path, article_id=self.article.id)

    def get_context_data(self, **kwargs):
        kwargs['attachment'] = self.attachment
        kwargs['selected_tab'] = 'attachments'
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(AttachmentDeleteView, self).get_context_data(**kwargs)


class AttachmentSearchView(ArticleMixin, ListView):

    template_name = "wiki/plugins/attachments/search.html"
    allow_empty = True
    context_object_name = 'attachments'
    paginator_class = WikiPaginator
    paginate_by = 10

    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(AttachmentSearchView, self).dispatch(request, article, *args, **kwargs)

    def get_queryset(self):
        self.query = self.request.GET.get('query', None)
        if not self.query:
            qs = models.Attachment.objects.none()
        else:
            qs = models.Attachment.objects.active().can_read(self.request.user)
            qs = qs.filter(
                Q(original_filename__contains=self.query) |
                Q(current_revision__description__contains=self.query) |
                Q(article__current_revision__title__contains=self.query))
        return qs.order_by('original_filename')

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
