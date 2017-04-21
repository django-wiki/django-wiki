from __future__ import absolute_import, unicode_literals

from haystack import indexes
from wiki import models


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    modified = indexes.DateTimeField(model_attr='modified')

    # default because indexing fails with whoosh. see.
    # http://stackoverflow.com/questions/11995367/how-do-i-use-a-boolean-field-in-django-haystack-search-query
    # https://github.com/toastdriven/django-haystack/issues/382
    other_read = indexes.BooleanField(model_attr='other_read', default=False)
    group_read = indexes.BooleanField(model_attr='group_read', default=False)

    owner_id = indexes.IntegerField(model_attr='owner__id', null=True)
    group_id = indexes.IntegerField(model_attr='group__id', null=True)

    def get_model(self):
        return models.Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
