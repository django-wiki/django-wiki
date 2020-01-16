import logging

from django.views.generic.base import TemplateResponseMixin
from wiki.conf import settings
from wiki.core.plugins import registry

log = logging.getLogger(__name__)


class ArticleMixin(TemplateResponseMixin):

    """A mixin that receives an article object as a parameter (usually from a wiki
    decorator) and puts this information as an instance attribute and in the
    template context."""

    def dispatch(self, request, article, *args, **kwargs):
        self.urlpath = kwargs.pop("urlpath", None)
        self.article = article
        self.children_slice = []
        if settings.SHOW_MAX_CHILDREN > 0:
            try:
                for child in self.article.get_children(
                    max_num=settings.SHOW_MAX_CHILDREN + 1,
                    articles__article__current_revision__deleted=False,
                    user_can_read=request.user,
                ):
                    self.children_slice.append(child)
            except AttributeError as e:
                log.error(
                    "Attribute error most likely caused by wrong MPTT version. Use 0.5.3+.\n\n"
                    + str(e)
                )
                raise
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs["urlpath"] = self.urlpath
        kwargs["article"] = self.article
        kwargs["article_tabs"] = registry.get_article_tabs()
        kwargs["children_slice"] = self.children_slice[:20]
        kwargs["children_slice_more"] = len(self.children_slice) > 20
        kwargs["plugins"] = registry.get_plugins()
        return kwargs
