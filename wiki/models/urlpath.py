# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.sites.models import Site
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from wiki.core.exceptions import NoRootURL, MultipleRootURLs
from wiki.conf import settings

from article import Article
from wiki.models.article import ArticleRevision, ArticleForObject
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError

class URLPath(MPTTModel):
    """
    Strategy: Very few fields go here, as most has to be managed through an
    article's revision. As a side-effect, the URL resolution remains slim and swift.
    """
    # Tells django-wiki that permissions from a URLPath object's article
    # should be inherited to children's articles
    INHERIT_PERMISSIONS = True 
    
    articles = generic.GenericRelation(ArticleForObject)
    slug = models.SlugField(verbose_name=_(u'slug'), null=True, blank=True)
    site = models.ForeignKey(Site)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')    
    
    def get_path(self):
        "/".join([obj.slug for obj in self.get_ancestors(include_self=True)])

    class MPTTMeta:
        pass
    
    def __unicode__(self):
        path = self.get_path()
        return path if path else ugettext(u"(root)")
    
    def save(self, *args, **kwargs):
        super(URLPath, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = _(u'URL path')
        verbose_name_plural = _(u'URL paths')
        unique_together = ('site', 'parent', 'slug')
        app_label = settings.APP_LABEL
    
    def clean(self, *args, **kwargs):
        if self.slug and not self.parent:
            raise ValidationError(_(u'Sorry but you cannot have a root article with a slug.'))
        if not self.slug and self.parent:
            raise ValidationError(_(u'A non-root note must always have a slug.'))
        if not self.parent:
            if URLPath.objects.root_nodes().filter(site=self.site):
                raise ValidationError(_(u'There is already a root node on %s') % self.site)
        super(URLPath, self).clean(*args, **kwargs)
    
    @classmethod
    def get_by_path(cls, path):
        """
        Strategy: Don't handle all kinds of weird cases. Be strict.
        Accepts paths both starting with and without '/'
        """
        site = Site.objects.get_current()
        root_nodes = cls.objects.root_nodes().filter(site=site)
        path = path.lstrip("/")
        
        no_paths = root_nodes.count()
        if no_paths == 0:
            raise NoRootURL
        if no_paths > 1:
            raise MultipleRootURLs
        # Root page requested
        if not path:
            return root_nodes[0]
        
        slugs = path.split('/')
        level = 1
        parent = root_nodes[0]
        for slug in slugs:
            if settings.URL_CASE_SENSITIVE:
                parent = parent.get_children.get(slug=slug)
            else:
                parent = parent.get_children.get(slug__iexact=slug)
            level += 1
        
        return parent
    
    @classmethod
    def create_root(cls, site=None):
        if not site: site = Site.objects.get_current()
        if not cls.objects.root_nodes().filter(site=site):
            # (get_or_create does not work for MPTT models??)
            root = cls.objects.create(site=site)
            article = Article()
            article.add_revision(ArticleRevision(), save=True)
            article.add_object_relation(root)
    
    @property
    def article(self):
        try:
            return self.articles.all()[0]
        except IndexError:
            return None
    