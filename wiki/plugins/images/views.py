from wiki.views.mixins import ArticleMixin
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from wiki.decorators import get_article

class ImageView(ArticleMixin, TemplateView):
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(ImageView, self).dispatch(request, article, *args, **kwargs)

    