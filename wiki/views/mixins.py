from django.views.generic.base import TemplateResponseMixin
from wiki.core import plugins_registry

class ArticleMixin(TemplateResponseMixin):
    
    def dispatch(self, request, article, *args, **kwargs):
        self.urlpath = kwargs.pop('urlpath', None)
        self.article = article
        return super(ArticleMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['urlpath'] = self.urlpath
        kwargs['article'] = self.article
        kwargs['plugins'] = plugins_registry._cache.values()
        return kwargs
