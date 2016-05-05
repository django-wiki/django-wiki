from __future__ import absolute_import, unicode_literals

from django.utils.decorators import method_decorator
from django.views.generic.base import View
from wiki import models
from wiki.decorators import get_article, json_view


class QueryUrlPath(View):

    # TODO: get_article does not actually support JSON responses
    @method_decorator(json_view)
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        max_num = kwargs.pop('max_num', 20)
        # TODO: Move this import when circularity issue is resolved
        # https://github.com/django-wiki/django-wiki/issues/23
        query = request.GET.get('query', None)

        if query:
            matches = models.URLPath.objects.can_read(
                request.user).active().filter(
                article__current_revision__title__contains=query,
                article__current_revision__deleted=False,
            )
            matches = matches.select_related_common()
            return [("[%s](wiki:%s)") %
                    (m.article.current_revision.title, '/' +
                     m.path.strip("/")) for m in matches[:max_num]]

        return []
