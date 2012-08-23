from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet, EmptyQuerySet
from mptt.managers import TreeManager

class ArticleEmptyQuerySet(QuerySet):
    def can_read(self, user):
        return self
    def can_write(self, user):
        return self
    def active(self):
        return self

class ArticleQuerySet(QuerySet):
    
    def can_read(self, user):
        """Filter objects so only the ones with a user's reading access
        are included"""
        if user.has_perm('wiki.moderator'):
            return self
        if user.is_anonymous():
            q = self.filter(other_read=True)
        else:
            q = self.filter(Q(other_read=True) |
                            Q(owner=user) |
                            (Q(group__user=user) & Q(group_read=True))
                            )
        return q
    
    def can_write(self, user):
        """Filter objects so only the ones with a user's writing access
        are included"""
        if user.has_perm('wiki.moderator'):
            return self
        if user.is_anonymous():
            q = self.filter(other_write=True)
        else:
            q = self.filter(Q(other_write=True) |
                            Q(owner=user) |
                            (Q(group__user=user) & Q(group_write=True))
                            )
        return q
    
    def active(self):
        return self.filter(current_revision__deleted=False)

class ArticleFkQuerySetMixin():
    
    def can_read(self, user):
        """Filter objects so only the ones with a user's reading access
        are included"""
        if user.has_perm('wiki.moderate'):
            return self
        if user.is_anonymous():
            q = self.filter(article__other_read=True)
        else:
            q = self.filter(Q(article__other_read=True) |
                            Q(article__owner=user) |
                            (Q(article__group__user=user) & Q(article__group_read=True))
                            )
        return q
    
    def can_write(self, user):
        """Filter objects so only the ones with a user's writing access
        are included"""
        if user.has_perm('wiki.moderate'):
            return self
        if user.is_anonymous():
            q = self.filter(article__other_write=True)
        else:
            q = self.filter(Q(article__other_write=True) |
                            Q(article__owner=user) |
                            (Q(article__group__user=user) & Q(article__group_write=True))
                            )
        return q

    def active(self):
        return self.filter(article__current_revision__deleted=False)

class ArticleFkEmptyQuerySetMixin():
    def can_read(self, user):
        return self
    def can_write(self, user):
        return self
    def active(self):
        return self

class ArticleFkQuerySet(ArticleFkQuerySetMixin, QuerySet):
    pass

class ArticleFkEmptyQuerySet(ArticleFkEmptyQuerySetMixin, EmptyQuerySet):
    pass

class ArticleManager(models.Manager):
    def get_empty_query_set(self):
        return ArticleEmptyQuerySet(model=self.model)
    def get_query_set(self):
        return ArticleQuerySet(self.model, using=self._db)
    def active(self):
        return self.get_query_set().active()
    def can_read(self, user):
        return self.get_query_set().can_read(user)
    def can_write(self, user):
        return self.get_query_set().can_write(user)

class ArticleFkManager(models.Manager):
    def get_empty_query_set(self):
        return ArticleFkEmptyQuerySet(model=self.model)
    def get_query_set(self):
        return ArticleFkQuerySet(self.model, using=self._db)
    def active(self):
        return self.get_query_set().active()
    def can_read(self, user):
        return self.get_query_set().can_read(user)
    def can_write(self, user):
        return self.get_query_set().can_write(user)


class URLPathEmptyQuerySet(EmptyQuerySet, ArticleFkEmptyQuerySetMixin):

    def select_related_common(self):
        return self

class URLPathQuerySet(QuerySet, ArticleFkQuerySetMixin):
    
    def select_related_common(self):
        return self.select_related("parent", "article__current_revision", "article__owner")

class URLPathManager(TreeManager):
    
    def get_empty_query_set(self):
        return URLPathEmptyQuerySet(model=self.model)
    
    def get_query_set(self):
        """Return a QuerySet with the same ordering as the TreeManager."""
        return URLPathQuerySet(self.model, using=self._db).order_by(
            self.tree_id_attr, self.left_attr)
    
    def select_related_common(self):
        return self.get_query_set().common_select_related()
    def active(self):
        return self.get_query_set().active()
    def can_read(self, user):
        return self.get_query_set().can_read(user)
    def can_write(self, user):
        return self.get_query_set().can_write(user)
