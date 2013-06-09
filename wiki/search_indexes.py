from haystack.indexes import *
from haystack import site
from wiki import models 


class ArticleIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    created = DateTimeField(model_attr='created')
    modified = DateTimeField(model_attr='modified')
    #default because indexing fails with whoosh. see. 
    #http://stackoverflow.com/questions/11995367/how-do-i-use-a-boolean-field-in-django-haystack-search-query
    #https://github.com/toastdriven/django-haystack/issues/382
    other_read = BooleanField(model_attr='other_read',default=False)

    def get_model(self):
        return models.Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

site.register(models.Article, ArticleIndex)

