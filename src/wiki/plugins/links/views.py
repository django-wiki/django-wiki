from django.utils.decorators import method_decorator
from django.views.generic.base import View
from wiki import models
from wiki.core.utils import object_to_json_response
from wiki.decorators import get_article


class QueryUrlPath(View):

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        max_num = kwargs.pop('max_num', 20)
        query = request.GET.get('query', None)

        matches = []

        if query:
            matches = models.URLPath.objects.can_read(
                request.user).active().filter(
                article__current_revision__title__contains=query,
                article__current_revision__deleted=False,
            )
            matches = matches.select_related_common()
            matches = [
                "[{title:s}](wiki:{url:s})".format(
                    title=m.article.current_revision.title,
                    url='/' + m.path.strip("/")
                ) for m in matches[:max_num]
            ]

        return object_to_json_response(matches)
