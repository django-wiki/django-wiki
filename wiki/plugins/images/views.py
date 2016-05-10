from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from wiki.conf import settings as wiki_settings
from wiki.decorators import get_article
from wiki.models.pluginbase import RevisionPluginRevision
from wiki.plugins.images import forms, models
from wiki.views.mixins import ArticleMixin

logger = logging.getLogger(__name__)


class ImageView(ArticleMixin, ListView):

    template_name = 'wiki/plugins/images/index.html'
    allow_empty = True
    context_object_name = 'images'
    paginate_by = 10

    @method_decorator(get_article(can_read=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(
            ImageView,
            self).dispatch(
            request,
            article,
            *args,
            **kwargs)

    def get_queryset(self):
        if (self.article.can_moderate(self.request.user) or
                self.article.can_delete(self.request.user)):
            images = models.Image.objects.filter(article=self.article)
        else:
            images = models.Image.objects.filter(
                article=self.article,
                current_revision__deleted=False)
        images.select_related()
        return images

    def get_context_data(self, **kwargs):
        kwargs.update(ArticleMixin.get_context_data(self, **kwargs))
        return ListView.get_context_data(self, **kwargs)


class DeleteView(ArticleMixin, RedirectView):

    permanent = False

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.image = get_object_or_404(models.Image, article=article,
                                       id=kwargs.get('image_id', None))
        self.restore = kwargs.get('restore', False)
        return ArticleMixin.dispatch(self, request, article, *args, **kwargs)

    def get_redirect_url(self, **kwargs):

        if not self.image.current_revision:
            logger.critical('Encountered an image without current revision set, ID: {}'.format(self.image.id))
            latest_revision = RevisionPluginRevision.objects.filter(
                plugin=self.image
            ).latest('pk')
            self.image.current_revision = latest_revision

        new_revision = models.ImageRevision()
        new_revision.inherit_predecessor(self.image)
        new_revision.set_from_request(self.request)
        new_revision.revision_number = RevisionPluginRevision.objects.filter(plugin=self.image).count()
        new_revision.deleted = not self.restore
        new_revision.save()
        self.image.current_revision = new_revision
        self.image.save()
        if self.restore:
            messages.info(
                self.request,
                _('%s has been restored') %
                new_revision.get_filename())
        else:
            messages.info(
                self.request,
                _('%s has been marked as deleted') %
                new_revision.get_filename())
        if self.urlpath:
            return reverse(
                'wiki:images_index',
                kwargs={
                    'path': self.urlpath.path})
        return reverse(
            'wiki:images_index',
            kwargs={
                'article_id': self.article.id})


class PurgeView(ArticleMixin, FormView):

    template_name = "wiki/plugins/images/purge.html"
    permanent = False
    form_class = forms.PurgeForm

    @method_decorator(get_article(can_write=True, can_moderate=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.image = get_object_or_404(models.Image, article=article,
                                       id=kwargs.get('image_id', None))
        return ArticleMixin.dispatch(self, request, article, *args, **kwargs)

    def form_valid(self, form):

        for revision in self.image.revision_set.all().select_related(
                "imagerevision"):
            revision.imagerevision.image.delete(save=False)
            revision.imagerevision.delete()

        if self.urlpath:
            return redirect('wiki:images_index', path=self.urlpath.path)
        return redirect('wiki:images_index', article_id=self.article_id)

    def get_context_data(self, **kwargs):
        # Needed since Django 1.9 because get_context_data is no longer called
        # with the form instance
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs = ArticleMixin.get_context_data(self, **kwargs)
        kwargs.update(FormView.get_context_data(self, **kwargs))
        return kwargs


class RevisionChangeView(ArticleMixin, RedirectView):

    permanent = False

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.image = get_object_or_404(models.Image, article=article,
                                       id=kwargs.get('image_id', None))
        self.revision = get_object_or_404(
            models.ImageRevision,
            plugin__article=article,
            id=kwargs.get(
                'rev_id',
                None))
        return ArticleMixin.dispatch(self, request, article, *args, **kwargs)

    def get_redirect_url(self, **kwargs):

        self.image.current_revision = self.revision
        self.image.save()
        messages.info(
            self.request,
            _('%(file)s has been changed to revision #%(revision)d') % {
                'file': self.image.current_revision.imagerevision.get_filename(),
                'revision': self.revision.revision_number})
        if self.urlpath:
            return reverse(
                'wiki:images_index',
                kwargs={
                    'path': self.urlpath.path})
        return reverse(
            'wiki:images_index',
            kwargs={
                'article_id': self.article.id})


class RevisionAddView(ArticleMixin, FormView):

    template_name = "wiki/plugins/images/revision_add.html"
    form_class = forms.RevisionForm

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.image = get_object_or_404(models.Image, article=article,
                                       id=kwargs.get('image_id', None))
        if not self.image.can_write(request.user):
            return redirect(wiki_settings.LOGIN_URL)
        return ArticleMixin.dispatch(self, request, article, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        kwargs = super(RevisionAddView, self).get_form_kwargs(**kwargs)
        kwargs['image'] = self.image
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        # Needed since Django 1.9 because get_context_data is no longer called
        # with the form instance
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs = super(RevisionAddView, self).get_context_data(**kwargs)
        kwargs['image'] = self.image
        return kwargs

    def form_valid(self, form, **kwargs):
        form.save()
        messages.info(
            self.request, _('%(file)s has been saved.') %
            {'file': self.image.current_revision.imagerevision.get_filename(), })
        if self.urlpath:
            return redirect('wiki:edit', path=self.urlpath.path)
        return redirect('wiki:edit', article_id=self.article.id)
