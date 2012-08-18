from django.views.generic.list import ListView
from django.utils.decorators import method_decorator

from wiki.decorators import get_article
from wiki.views.mixins import ArticleMixin

from wiki.plugins.images import models

class ImageView(ArticleMixin, ListView):
    
    template_name = 'wiki/plugins/images/index.html'
    allow_empty = True
    context_object_name = 'images'
    paginate_by = 10
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(ImageView, self).dispatch(request, article, *args, **kwargs)
    
    def get_queryset(self):
        return models.Image.objects.filter(article=self.article)
    
    def get_context_data(self, **kwargs):
        kwargs.update(ArticleMixin.get_context_data(self, **kwargs))
        return ListView.get_context_data(self, **kwargs)
    