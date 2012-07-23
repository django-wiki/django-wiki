# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from wiki.core.exceptions import NoRootURL, MultipleRootURLs
from wiki.conf import settings

class URLPath(MPTTModel):
    """
    Strategy: Very few fields go here, as most has to be managed through an
    article's revision. As a side-effect, the URL resolution remains slim and swift.
    """
    article = models.ForeignKey('Article',
                                verbosen_name=_(u'article'),
                                help_text=_(u'Article to be displayed for this path'))
    slug = models.SlugField(verbose_name=_(u'slug'))
    site = models.ForeignKey(Site)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')    
    
    def get_path(self):
        "/".join([obj.slug for obj in self.get_ancestors(include_self=True)])

    class MPTTMeta:
        order_insertion_by = ['slug']
    
    def __unicode__(self):
        return self.path
    
    def save(self, *args, **kwargs):
        super(URLPath, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = _(u'URL path')
        verbose_name_plural = _(u'URL paths')
        unique_together = ('site', 'parent', 'slug')
        
    @classmethod
    def get_by_path(cls, path):
        """
        Strategy: Don't handle all kinds of weird cases. Be strict.
        Accepts paths both starting with and without '/'
        """
        site = Site.objects.get_current()
        paths = cls.objects.filter(site=site)
        root_nodes = paths.filter(parent=None)
        path = path.lstrip("/")
        
        # Root page requested
        if not path:
            no_paths = root_nodes.count()
            if no_paths == 0:
                raise NoRootURL
            if no_paths > 1:
                raise MultipleRootURLs
            return root_nodes[0]
        
        slugs = path.split('/')
        for slug in slugs:
            if settings.URL_CASE_SENSITIVE:
                paths = paths.filter(parent__slug=slug)
            else:
                paths = paths.filter(parent__slug__iexact=slug)
        
        if paths.count() == 0:
            raise cls.DoesNotExist
        
        return paths[0]
        