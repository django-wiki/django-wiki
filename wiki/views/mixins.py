from django.views.generic.base import TemplateResponseMixin

from wiki.core import plugins_registry

class ArticleMixin(TemplateResponseMixin):
    """A mixin that receives an article object as a parameter (usually from a wiki
    decorator) and puts this information as an instance attribute and in the
    template context."""
    
    def dispatch(self, request, article, *args, **kwargs):
        self.urlpath = kwargs.pop('urlpath', None)
        self.article = article        
        return super(ArticleMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['urlpath'] = self.urlpath
        kwargs['article'] = self.article
        kwargs['plugins'] = plugins_registry._cache.values()
        return kwargs
