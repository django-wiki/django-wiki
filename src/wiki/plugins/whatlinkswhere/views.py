from urllib.parse import quote as urlquote

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView
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
    template_name = "wiki/plugins/whatlinkswhere/whatlinkshere.html"
    allow_empty = True
    context_object_name = "whatlinkswhere"
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
        return self.model.objects.filter(to_article=self.article)

    def get_context_data(self, **kwargs):
        # Apparently a standard hack for (ListView, ArticleMixin) classes
        kwargs_article = ArticleMixin.get_context_data(self, **kwargs)
        kwargs_listview = ListView.get_context_data(self, **kwargs)
        kwargs.update(kwargs_article)
        kwargs.update(kwargs_listview)
        return kwargs


class WhatLinksWhere(ListView):
    template_name = "wiki/plugins/whatlinkswhere/whatlinkswhere.html"
    allow_empty = True
    context_object_name = "whatlinkswhere"
    paginator_class = WikiPaginator
    paginate_by = 50
    model = models.InternalLink

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter()

    def get_context_data(self, **kwargs):
        # Is this a bit of a hack? Use better inheritance?
        return super().get_context_data(**kwargs)
