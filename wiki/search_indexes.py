from haystack.indexes import *
from haystack import site
from wiki import models 


class ArticleIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    created = DateTimeField(model_attr='created')
    modified = DateTimeField(model_attr='modified')

    def get_model(self):
        return models.Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

site.register(models.Article, ArticleIndex)

