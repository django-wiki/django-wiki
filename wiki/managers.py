from django.db import models
from django.db.models import Q

class PermissionArticleManagerMixin(object):
    
    def can_read(self, user):
        """Filter objects so only the ones with a user's reading access
        are included"""
        if user.has_perm('wiki.moderator'):
            return self.get_query_set()
        q = self.get_query_set().filter(Q(other_read=True) |
                                        Q(owner=user) |
                                        (Q(group__user=user) & Q(group_read=True))
                                        )
        return q
    
    def can_write(self, user):
        """Filter objects so only the ones with a user's writing access
        are included"""
        if user.has_perm('wiki.moderator'):
            return self.get_query_set()
        q = self.get_query_set().filter(Q(other_write=True) |
                                        Q(owner=user) |
                                        (Q(group__user=user) & Q(group_write=True))
                                        )
        return q

class PermissionArticleManager(PermissionArticleManagerMixin, models.Manager):
    pass

class PermissionArticleFkManagerMixin(object):
    """A manager like the above but for objects that have a ForeignKey to
    an article object and inherits its permissions."""
    
    def can_read(self, user):
        """Filter objects so only the ones with a user's reading access
        are included"""
        if user.has_perm('wiki.moderator'):
            return self.get_query_set()
        q = self.get_query_set().filter(Q(article__other_read=True) |
                                        Q(article__owner=user) |
                                        (Q(article__group__user=user) & Q(article__group_read=True))
                                        )
        return q
    
    def can_write(self, user):
        """Filter objects so only the ones with a user's writing access
        are included"""
        if user.has_perm('wiki.moderator'):
            return self.get_query_set()
        q = self.get_query_set().filter(Q(article__other_write=True) |
                                        Q(article__owner=user) |
                                        (Q(article__group__user=user) & Q(article__group_write=True))
                                        )
        return q

class PermissionArticleFkManager(models.Manager, PermissionArticleFkManagerMixin):
    pass

class ActiveObjectsManager(models.Manager, PermissionArticleManagerMixin):
    """A manager for objects that have a ForeignKey named 'current_revision' 
    (ie. a BaseRevision inheritor)."""
    
    def get_query_set(self):
        return super(ActiveObjectsManager, self).get_query_set().filter(current_revision__deleted=False)

class ActiveObjectsFkManager(ActiveObjectsManager, PermissionArticleFkManagerMixin):
    pass

