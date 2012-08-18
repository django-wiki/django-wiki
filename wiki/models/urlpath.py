# -*- coding: utf-8 -*-
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.utils.translation import ugettext_lazy as _, ugettext

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from wiki.conf import settings
from wiki.core.exceptions import NoRootURL, MultipleRootURLs
from wiki.models.article import ArticleRevision, ArticleForObject, Article
from django.contrib.contenttypes.models import ContentType

class URLPath(MPTTModel):
    """
    Strategy: Very few fields go here, as most has to be managed through an
    article's revision. As a side-effect, the URL resolution remains slim and swift.
    """
    # Tells django-wiki that permissions from a this object's article
    # should be inherited to children's articles. In this case, it's a static
    # property.. but you can also use a BooleanField.
    INHERIT_PERMISSIONS = True 
    
    articles = generic.GenericRelation(ArticleForObject)
    
    # Do NOT modify this field - it is updated with signals whenever ArticleForObject is changed.
    article = models.ForeignKey(Article, on_delete=models.CASCADE, editable=False,
                                verbose_name=_(u'Cache lookup value for articles'))
    
    slug = models.SlugField(verbose_name=_(u'slug'), null=True, blank=True)
    site = models.ForeignKey(Site)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')    
    
    @property
    def path(self):
        if not self.parent: return ""
        if not hasattr(self, '_cachedpath'):
            self._cachedpath = "/".join([obj.slug if obj.slug else "" for obj in self.get_ancestors(include_self=True).exclude(parent=None)]) + "/"
        return self._cachedpath 
    
    @classmethod
    def root(cls):
        site = Site.objects.get_current()
        root_nodes = list(cls.objects.root_nodes().filter(site=site))
        # We fetch the nodes as a list and use len(), not count() because we need
        # to get the result out anyway. This only takes one sql query
        no_paths = len(root_nodes)
        if no_paths == 0:
            raise NoRootURL("You need to create a root article on site '%s'" % site)
        if no_paths > 1:
            raise MultipleRootURLs("Somehow you have multiple roots on %s" % site)
        return root_nodes[0]

    class MPTTMeta:
        pass
    
    def __unicode__(self):
        path = self.path
        return path if path else ugettext(u"(root)")
    
    def save(self, *args, **kwargs):
        super(URLPath, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        assert not (self.parent and self.get_children()), "You cannot delete a root article with children."
        super(URLPath, self).delete(*args, **kwargs)
    
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
            if URLPath.objects.root_nodes().filter(site=self.site).exclude(id=self.id):
                raise ValidationError(_(u'There is already a root node on %s') % self.site)
        super(URLPath, self).clean(*args, **kwargs)
    
    @classmethod
    def get_by_path(cls, path, select_related=False):
        """
        Strategy: Don't handle all kinds of weird cases. Be strict.
        Accepts paths both starting with and without '/'
        """
        
        # TODO: Save paths directly in the model for constant time lookups?
        
        # Or: Save the parents in a lazy property because the parents are
        # always fetched anyways so it's fine to fetch them here.
        path = path.lstrip("/")
        path = path.rstrip("/")
        
        # Root page requested
        if not path:
            return cls.root()
        
        slugs = path.split('/')
        level = 1
        parent = cls.root()
        for slug in slugs:
            if settings.URL_CASE_SENSITIVE:
                parent = parent.get_children().get(slug=slug)
            else:
                parent = parent.get_children().get(slug__iexact=slug)
            level += 1
                
        return parent
    
    def get_absolute_url(self):
        return reverse('wiki:get_url', args=(self.path,))
    
    @classmethod
    def create_root(cls, site=None, title="Root", **kwargs):
        if not site: site = Site.objects.get_current()
        root_nodes = cls.objects.root_nodes().filter(site=site)
        if not root_nodes:
            # (get_or_create does not work for MPTT models??)
            article = Article()
            article.add_revision(ArticleRevision(title=title, **kwargs),
                                 save=True)
            article.save()
            root = cls.objects.create(site=site, article=article)
            article.add_object_relation(root)
        else:
            root = root_nodes[0]
        return root
        
    @classmethod
    def create_article(cls, parent, slug, site=None, title="Root", article_kwargs={}, **kwargs):
        """Utility function:
        Create a new urlpath with an article and a new revision for the article"""
        if not site: site = Site.objects.get_current()
        article = Article(**article_kwargs)
        article.add_revision(ArticleRevision(title=title, **kwargs),
                             save=True)
        article.save()
        newpath = cls.objects.create(site=site, parent=parent, slug=slug, article=article)
        article.add_object_relation(newpath)
        return newpath
    

######################################################
# SIGNAL HANDLERS
######################################################

# Just get this once
urlpath_content_type = None

def on_article_relation_save(instance, *args, **kwargs):
    global urlpath_content_type
    if not urlpath_content_type:
        urlpath_content_type = ContentType.objects.get_for_model(URLPath)
    if instance.content_type == urlpath_content_type:
        URLPath.objects.filter(id=instance.object_id).update(article=instance.article)

post_save.connect(on_article_relation_save, ArticleForObject)

def on_article_delete(instance, *args, **kwargs):
    # If an article is deleted, then throw out its URLPaths
    # But move all descendants to a lost-and-found node.
    site = Site.objects.get_current()
    
    # Get the Lost-and-found path or create a new one
    try:
        lost_and_found = URLPath.objects.get(slug=settings.LOST_AND_FOUND_SLUG,
                                             parent=URLPath.root(),
                                             site=site)
    except URLPath.DoesNotExist:
        lost_and_found = URLPath.objects.create(slug=settings.LOST_AND_FOUND_SLUG,
                                                parent=URLPath.root(),
                                                site=site,)
        article = Article(group_read = True,
                          group_write = False,
                          other_read = False,
                          other_write = False)
        article.add_revision(ArticleRevision(
                 content=_(u'Articles who lost their parents'
                            '==============================='),
                 title=_(u"Lost and found")))
    
    for urlpath in URLPath.objects.filter(articles__article=instance, site=site):
        # Delete the children
        for child in urlpath.get_children():
            child.move_to(lost_and_found)
        # ...and finally delete the path itself
        # TODO: This should be unnecessary because of URLPath.article(...ondelete=models.CASCADE)
        urlpath.delete()
    
pre_delete.connect(on_article_delete, Article)
