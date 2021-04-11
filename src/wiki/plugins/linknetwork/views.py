from urllib.parse import quote as urlquote

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.views.generic import View
from wiki import models as wiki_models
from wiki.conf import settings
from wiki.core.paginator import WikiPaginator
from wiki.decorators import get_article
from wiki.views.mixins import ArticleMixin

from . import models


def response_forbidden(request, article, urlpath, read_denied=False):
    if request.user.is_anonymous:
        qs = request.META.get("QUERY_STRING", "")
        if qs:
            qs = urlquote("?" + qs)
        else:
            qs = ""
        return redirect(settings.LOGIN_URL + "?next=" + request.path + qs)
    else:
        return HttpResponseForbidden(
            render_to_string(
                "wiki/permission_denied.html",
                context={
                    "article": article,
                    "read_denied": read_denied,
                },
                request=request,
            )
        )


class WhatLinksHere(ListView, ArticleMixin):
    template_name = "wiki/plugins/linknetwork/whatlinkshere.html"
    allow_empty = True
    context_object_name = "linknetwork"
    paginator_class = WikiPaginator
    paginate_by = 50
    model = models.InternalLink

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        # If the article has been deleted, show a special page.
        if article.current_revision and article.current_revision.deleted:
            return redirect("wiki:deleted", article_id=article.id)

        if not article.can_read(request.user):
            return response_forbidden(request, article, read_denied=True)

        return super().dispatch(request, article, *args, **kwargs)

    def get_queryset(self):
        # TODO: This filter should use query logic, instead of python filtering, as much as possible.
        return [
            link
            for link in self.model.objects.filter(to_article=self.article).all()
            if link.from_article.can_read(self.request.user)
        ]

    def get_context_data(self, **kwargs):
        # Apparently a standard hack for (ListView, ArticleMixin) classes
        kwargs_article = ArticleMixin.get_context_data(self, **kwargs)
        kwargs_listview = ListView.get_context_data(self, **kwargs)
        kwargs.update(kwargs_article)
        kwargs.update(kwargs_listview)
        return kwargs


class LinkNetwork(ListView, ArticleMixin):
    template_name = "wiki/plugins/linknetwork/linknetwork.html"
    allow_empty = True
    context_object_name = "linknetwork"
    paginator_class = WikiPaginator
    paginate_by = 50
    model = models.InternalLink

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        if not article.can_read(request.user):
            return response_forbidden(request, article, read_denied=True)
        return super().dispatch(request, article, *args, **kwargs)

    def get_queryset(self):
        self.nodes = [
            article
            for article in wiki_models.Article.objects.all()
            if article.get_absolute_url().startswith(self.article.get_absolute_url())
            if article.can_read(self.request.user)
        ]
        # For network display of the namespace, it would be nice to also pass
        # the isolated nodes, with no outgoing and no incoming edges. That
        # would probably also require de-activating the paginator.
        return self.model.objects.filter(
            Q(from_article__in=self.nodes)
            & (
                Q(to_article__in=self.nodes)
                | Q(to_nonexistant_url__startswith=self.article.get_absolute_url())
            )
        )

    def get_context_data(self, **kwargs):
        # Apparently a standard hack for (ListView, ArticleMixin) classes
        kwargs_article = ArticleMixin.get_context_data(self, **kwargs)
        kwargs_listview = ListView.get_context_data(self, **kwargs)
        kwargs.update(kwargs_article)
        kwargs.update(kwargs_listview)
        return kwargs


class GlobalUpdate(View):
    def dispatch(self, request, *args, **kwargs):
        for article in wiki_models.Article.objects.all():
            models.store_links(article.current_revision)
        messages.info(request, _("All internal links have been updated."))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return redirect("wiki:root")
