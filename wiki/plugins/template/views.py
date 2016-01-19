# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import View, TemplateView as DjTemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from wiki import editors
from wiki.conf import settings as wiki_settings
from wiki.decorators import json_view, get_article, response_forbidden
from wiki.plugins.template import models, settings, forms
from wiki.views.mixins import ArticleMixin


class TemplateCreateView(ArticleMixin, FormView):

    form_class = forms.TemplateForm
    template_name = "wiki/plugins/template/template_create.html"

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(TemplateCreateView, self).dispatch(request, article, *args, **kwargs)

    def form_valid(self, form):
        if (self.request.user.is_anonymous() and
                not settings.ANONYMOUS or
                not self.article.can_write(self.request.user) or
                self.article.current_revision.locked):
            return response_forbidden(self.request, self.article, self.urlpath)
        template_revision = form.save()
        messages.success(
            self.request,
            _('%s was successfully added.') % template_revision.template.template_title
        )
        return redirect(
            "wiki:template_index",
            path=self.urlpath.path,
            article_id=self.article.id
        )

    def get_form_kwargs(self):
        kwargs = FormView.get_form_kwargs(self)
        kwargs['article'] = self.article
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['selected_tab'] = 'template'
        kwargs['editor'] = editors.getEditor()
        return super(TemplateCreateView, self).get_context_data(**kwargs)


class TemplateView(ArticleMixin, DjTemplateView):

    template_name = "wiki/plugins/template/index.html"

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.template = models.Template.get_by_article(
            article).order_by('template_title')

        # Fixing some weird transaction issue caused by adding commit_manually
        # to form_valid
        return super(TemplateView, self).dispatch(request, article, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['templates'] = self.template
        kwargs['deleted_template'] = models.Template.objects.filter(
            articles=self.article, current_revision__deleted=True)
        kwargs['search_form'] = forms.SearchForm()
        kwargs['selected_tab'] = 'template'
        kwargs['anonymous_disallowed'] = self.request.user.is_anonymous(
        ) and not settings.ANONYMOUS_CREATE
        return super(TemplateView, self).get_context_data(**kwargs)


class EditPreview(ArticleMixin, DjTemplateView):

    template_name = "wiki/preview_inline.html"

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.template = get_object_or_404(
            models.Template,
            id=kwargs.get('template_id', None)
        )
        self.preview = kwargs.get('preview', True)
        if not self.template.can_write(request.user):
            return redirect(wiki_settings.LOGIN_URL)
        return ArticleMixin.dispatch(self, request, article, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        edit_form = forms.RevisionForm(
            request.POST,
            request=request,
            template=self.template
        )
        if edit_form.is_valid():
            self.title = self.template.template_title
            self.template_content = edit_form.cleaned_data['template_content']
            self.preview = True
        return super(EditPreview, self).get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.template and not self.title:
            self.title = self.template.title
        if self.template and not self.template_content:
            self.template_content = self.template.current_revision.template_content
        return super(EditPreview, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['title'] = _(
            'Preview Template: %s'
        ) % self.template.template_title
        kwargs['revision'] = None
        kwargs['content'] = self.template_content
        kwargs['preview'] = self.preview
        return ArticleMixin.get_context_data(self, **kwargs)


class CreatePreview(ArticleMixin, FormView):

    template_name = "wiki/preview_inline.html"
    form_class = forms.TemplateForm

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.preview = kwargs.get('preview', True)
        return ArticleMixin.dispatch(self, request, article, *args, **kwargs)

    def form_valid(self, form):
        self.title = form.cleaned_data['template_title']
        self.template_content = form.cleaned_data['template_content']
        self.preview = True
        return super(CreatePreview, self).get(self.request, *self.args, **self.kwargs)

    def get_context_data(self, **kwargs):
        kwargs['title'] = _(
            'Preview Template: %s'
        ) % self.title
        kwargs['revision'] = None
        kwargs['content'] = self.template_content
        kwargs['preview'] = self.preview
        return ArticleMixin.get_context_data(self, **kwargs)


class TemplateHistoryView(ArticleMixin, DjTemplateView):

    template_name = "wiki/plugins/template/history.html"

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, template_id, *args, **kwargs):
        if article.can_moderate(request.user):
            self.template = get_object_or_404(
                models.Template,
                id=template_id,
                articles=article
            )
        else:
            self.template = get_object_or_404(
                models.Template.objects.active(),
                id=template_id,
                articles=article
            )
        return super(TemplateHistoryView, self).dispatch(request, article, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['template'] = self.template
        kwargs['revisions'] = self.template.templaterevision_set.all(
        ).order_by('-revision_number')
        kwargs['selected_tab'] = 'template'
        return super(TemplateHistoryView, self).get_context_data(**kwargs)


class TemplateChangeRevisionView(ArticleMixin, View):

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, template_id, revision_id, *args, **kwargs):
        if article.can_moderate(request.user):
            self.template = get_object_or_404(
                models.Template,
                id=template_id,
                articles=article
            )
        else:
            self.template = get_object_or_404(
                models.Template.objects.active(),
                id=template_id,
                articles=article
            )
        self.revision = get_object_or_404(
            models.TemplateRevision,
            id=revision_id,
            template__articles=article
        )
        return super(TemplateChangeRevisionView, self).dispatch(request, article, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.template.current_revision = self.revision
        self.template.save()
        messages.success(
            self.request,
            _('Current revision changed for # %s.') % self.revision.revision_number
        )

        return redirect(
            "wiki:template_history",
            path=self.urlpath.path,
            article_id=self.article.id,
            template_id=self.template.id
        )


class RevisionAddView(ArticleMixin, FormView):

    template_name = "wiki/plugins/template/revision_add.html"
    form_class = forms.RevisionForm

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.template = get_object_or_404(
            models.Template,
            id=kwargs.get('template_id', None)
        )
        if not self.template.can_write(request.user):
            return redirect(wiki_settings.LOGIN_URL)
        return ArticleMixin.dispatch(self, request, article, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        kwargs = super(RevisionAddView, self).get_form_kwargs(**kwargs)
        kwargs['template'] = self.template
        kwargs['request'] = self.request
        kwargs['initial'] = {
            'template_content': self.template.current_revision.template_content
        }
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs = super(RevisionAddView, self).get_context_data(**kwargs)
        kwargs['template'] = self.template
        kwargs['editor'] = editors.getEditor()
        kwargs['selected_tab'] = 'template'
        return kwargs

    def form_valid(self, form, **kwargs):
        form.save()
        messages.info(
            self.request,
            _('%(template)s has been saved.') % {
                'template': self.template.template_title,
            }
        )
        return redirect(
            'wiki:template_index',
            path=self.urlpath.path,
            article_id=self.template.article.id
        )


class TemplateAddView(ArticleMixin, View):

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, template_id, *args, **kwargs):
        self.template = get_object_or_404(
            models.Template.objects.active().can_write(request.user),
            id=template_id
        )
        return super(TemplateAddView, self).dispatch(request, article, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.template.articles.filter(id=self.article.id):
            self.template.articles.add(self.article)
            self.template.save()
        messages.success(
            self.request,
            _('Added a reference to "%(template_title)s" from "%(article_title)s".') %
            {
                'template_title': self.template.template_title,
                'article_title': self.article.current_revision.title
            }
        )
        return redirect(
            "wiki:template_index",
            path=self.urlpath.path,
            article_id=self.article.id
        )


class TemplateDeleteView(ArticleMixin, FormView):

    form_class = forms.DeleteForm
    template_name = "wiki/plugins/template/delete.html"

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, template_id, *args, **kwargs):
        self.template = get_object_or_404(
            models.Template,
            id=template_id,
            articles=article
        )
        self.article = article
        if not self.template.can_delete(request.user):
            return response_forbidden(request, article, kwargs.get('urlpath', None))
        return super(TemplateDeleteView, self).dispatch(request, article, *args, **kwargs)

    def form_valid(self, form):

        if self.template.article == self.article:
            revision = models.TemplateRevision()
            revision.template = self.template
            revision.set_from_request(self.request)
            revision.deleted = True
            revision.template_content = self.template.current_revision.template_content if self.template.current_revision else ""
            revision.description = self.template.current_revision.description if self.template.current_revision else ""
            revision.save()
            self.template.current_revision = revision
            self.template.save()
            messages.info(
                self.request,
                _('The template %s was deleted.') % self.template.template_title
            )
        else:
            self.template.articles.remove(self.article)
            messages.info(
                self.request,
                _('This article is no longer related to the template %s.') % self.template.template_title
            )

        return redirect(
            "wiki:template_index",
            path=self.urlpath.path,
            article_id=self.article.id
        )

    def get_context_data(self, **kwargs):
        kwargs['template'] = self.template
        kwargs['selected_tab'] = 'template'
        return super(TemplateDeleteView, self).get_context_data(**kwargs)


class TemplateSearchView(ArticleMixin, ListView):

    template_name = "wiki/plugins/template/search.html"
    allow_empty = True
    context_object_name = 'templates'
    paginate_by = 10

    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(TemplateSearchView, self).dispatch(request, article, *args, **kwargs)

    def get_queryset(self):
        self.query = self.request.GET.get('query', None)
        if not self.query:
            qs = models.Template.objects.get_empty_query_set()
        else:
            qs = models.Template.objects.active().can_read(self.request.user)
            qs = qs.filter(
                Q(template_title__contains=self.query) |
                Q(current_revision__description__contains=self.query) |
                Q(article__current_revision__title__contains=self.query)
            )
        return qs

    def get_context_data(self, **kwargs):
        # Is this a bit of a hack? Use better inheritance?
        kwargs_article = ArticleMixin.get_context_data(self, **kwargs)
        kwargs_listview = ListView.get_context_data(self, **kwargs)
        kwargs['search_form'] = forms.SearchForm(self.request.GET)
        kwargs['query'] = self.query
        kwargs.update(kwargs_article)
        kwargs.update(kwargs_listview)
        kwargs['selected_tab'] = 'template'
        return kwargs


class QueryTitle(View):

    @method_decorator(json_view)
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        max_num = kwargs.pop('max_num', 20)
        # TODO: Move this import when circularity issue is resolved
        # https://github.com/benjaoming/django-wiki/issues/23
        query = request.GET.get('query', None)

        if query:
            matches = models.Template.get_by_article(article).can_read(request.user).active().filter(
                template_title__contains=query,
                article__current_revision__deleted=False,
            )
            # matches = matches.select_related_common()
            return [m.md_tag for m in matches[:max_num]]

        return []
