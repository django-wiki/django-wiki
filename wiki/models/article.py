# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Article(models.Model):
    
    title = models.CharField(max_length=512, verbose_name=_(u'title'))
    current_revision = models.ForeignKey('ArticleRevision')
    
    def add_revision(self, new_revision, save=True):
        """
        Sets the properties of a revision and ensures its the current
        revision.
        """
        revisions = self.articlerevision_set.all()
        try:
            new_revision.revision_number = revisions.latest().revision_number + 1
        except ArticleRevision.DoesNotExist:
            new_revision.revision_number = 0
        new_revision.article = self
        new_revision.save()
        self.current_revision = new_revision
        self.save()

class ArticleRevision(models.Model):
    
    article = models.ForeignKey('Article', on_delete=models.CASCADE,)
    revision_number = models.IntegerField()
    
    # This is where the content goes, with whatever markup language is used
    content = models.TextField(blank=True)
    
    # Simple properties
    deleted = models.BooleanField(verbose_name=_(u'Article has been deleted'))
    
    # Allow a revision to redirect to another *article*. This 
    # way, we can redirects and still maintain old content.
    redirect = models.ForeignKey('Article', null=True, blank=True,
                                 verbose_name=_(u'redirect'),
                                 help_text=_(u'If set, the article will redirect to the contents of another article.'))