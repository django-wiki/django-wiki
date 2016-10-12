# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models.signals import post_save, pre_delete
# Django 1.6 transaction API, required for 1.8+
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from six.moves import filter  # @UnresolvedImport
from wiki import managers
from wiki.conf import settings
from wiki.core.compat import atomic, transaction_commit_on_success
from wiki.core.exceptions import MultipleRootURLs, NoRootURL
from wiki.decorators import disable_signal_for_loaddata
from wiki.models.article import Article, ArticleForObject, ArticleRevision

try:
    notrans = transaction.non_atomic_requests
except:
    notrans = transaction.commit_manually  # @UndefinedVariable

# Django 1.9 deprecation of contenttypes.generic
try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation



log = logging.getLogger(__name__)


@python_2_unicode_compatible
class URLPath(MPTTModel):

    """
    Strategy: Very few fields go here, as most has to be managed through an
    article's revision. As a side-effect, the URL resolution remains slim and swift.
    """
    # Tells django-wiki that permissions from a this object's article
    # should be inherited to children's articles. In this case, it's a static
    # property.. but you can also use a BooleanField.
    INHERIT_PERMISSIONS = True

    objects = managers.URLPathManager()

    # Do not use this because of
    # https://github.com/django-mptt/django-mptt/issues/369
    # _default_manager = objects

    articles = GenericRelation(
        ArticleForObject,
        content_type_field='content_type',
        object_id_field='object_id',
    )

    # Do NOT modify this field - it is updated with signals whenever
    # ArticleForObject is changed.
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name=_('Lookup value'),
        help_text=_(
            "This field is automatically updated, but you need to populate "
            "it when creating a new URL path."
        )
    )

    SLUG_MAX_LENGTH = 50

    slug = models.SlugField(verbose_name=_('slug'), null=True, blank=True,
                            max_length=SLUG_MAX_LENGTH)
    site = models.ForeignKey(Site)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        help_text=_("Position of URL path in the tree.")
    )

    def __init__(self, *args, **kwargs):
        pass
        # Fixed in django-mptt 0.5.3
        # self._tree_manager = URLPath.objects
        return super(URLPath, self).__init__(*args, **kwargs)

    def __cached_ancestors(self):
        """
        This returns the ancestors of this urlpath. These ancestors are hopefully
        cached from the article path lookup. Accessing a foreign key included in
        add_selecte_related on one of these ancestors will not occur an additional
        sql query, as they were retrieved with a select_related.

        If the cached ancestors were not set explicitly, they will be retrieved from
        the database.
        """
        if not self.get_ancestors().exists():
            self._cached_ancestors = []
        if not hasattr(self, "_cached_ancestors"):
            self._cached_ancestors = list(
                self.get_ancestors().select_related_common())

        return self._cached_ancestors

    def __cached_ancestors_setter(self, ancestors):
        self._cached_ancestors = ancestors

    # Python 2.5 compatible property constructor
    cached_ancestors = property(__cached_ancestors,
                                __cached_ancestors_setter)

    def set_cached_ancestors_from_parent(self, parent):
        self.cached_ancestors = parent.cached_ancestors + [parent]

    @property
    def path(self):
        if not self.parent:
            return ""

        ancestors = list(
            filter(
                lambda ancestor: ancestor.parent is not None,
                self.cached_ancestors))
        slugs = [obj.slug if obj.slug else "" for obj in ancestors + [self]]

        return "/".join(slugs) + "/"

    def is_deleted(self):
        """
        Returns True if this article or any of its ancestors have been deleted
        """
        return self.first_deleted_ancestor() is not None

    def first_deleted_ancestor(self):
        for ancestor in self.cached_ancestors + [self]:
            if ancestor.article.current_revision.deleted:
                return ancestor
        return None

    @atomic
    @transaction_commit_on_success
    def _delete_subtree(self):
        for descendant in self.get_descendants(
                include_self=True).order_by("-level"):
            descendant.article.delete()

    def delete_subtree(self):
        """
        NB! This deletes this urlpath, its children, and ALL of the related
        articles. This is a purged delete and CANNOT be undone.
        """
        try:
            self._delete_subtree()
        except:
            # Not sure why any exception is getting caught here? Have we had
            # unresolved database integrity errors?
            log.exception("Exception deleting article subtree.")

    @classmethod
    def root(cls):
        site = Site.objects.get_current()
        root_nodes = list(
            cls.objects.root_nodes().filter(site=site).select_related_common()
        )
        # We fetch the nodes as a list and use len(), not count() because we need
        # to get the result out anyway. This only takes one sql query
        no_paths = len(root_nodes)
        if no_paths == 0:
            raise NoRootURL(
                "You need to create a root article on site '%s'" %
                site)
        if no_paths > 1:
            raise MultipleRootURLs(
                "Somehow you have multiple roots on %s" %
                site)
        return root_nodes[0]

    class MPTTMeta:
        pass

    def __str__(self):
        path = self.path
        return path if path else ugettext("(root)")

    def delete(self, *args, **kwargs):
        assert not (self.parent and self.get_children()
                    ), "You cannot delete a root article with children."
        super(URLPath, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _('URL path')
        verbose_name_plural = _('URL paths')
        unique_together = ('site', 'parent', 'slug')

    def clean(self, *args, **kwargs):
        if self.slug and not self.parent:
            raise ValidationError(
                _('Sorry but you cannot have a root article with a slug.'))
        if not self.slug and self.parent:
            raise ValidationError(
                _('A non-root note must always have a slug.'))
        if not self.parent:
            if URLPath.objects.root_nodes().filter(
                    site=self.site).exclude(
                    id=self.id):
                raise ValidationError(
                    _('There is already a root node on %s') %
                    self.site)
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
                child = parent.get_children().select_related_common().get(
                    slug=slug)
                child.cached_ancestors = parent.cached_ancestors + [parent]
                parent = child
            else:
                child = parent.get_children().select_related_common().get(
                    slug__iexact=slug)
                child.cached_ancestors = parent.cached_ancestors + [parent]
                parent = child
            level += 1

        return parent

    def get_absolute_url(self):
        return reverse('wiki:get', kwargs={'path': self.path})

    @classmethod
    def create_root(cls, site=None, title="Root", request=None, **kwargs):
        if not site:
            site = Site.objects.get_current()
        root_nodes = cls.objects.root_nodes().filter(site=site)
        if not root_nodes:
            # (get_or_create does not work for MPTT models??)
            article = Article()
            revision = ArticleRevision(title=title, **kwargs)
            if request:
                revision.set_from_request(request)
            article.add_revision(revision, save=True)
            article.save()
            root = cls.objects.create(site=site, article=article)
            article.add_object_relation(root)
        else:
            root = root_nodes[0]
        return root

    @classmethod
    @atomic
    @transaction_commit_on_success
    def create_article(
            cls,
            parent,
            slug,
            site=None,
            title="Root",
            article_kwargs={},
            **kwargs):
        """Utility function:
        Create a new urlpath with an article and a new revision for the article"""
        if not site:
            site = Site.objects.get_current()
        article = Article(**article_kwargs)
        article.add_revision(ArticleRevision(title=title, **kwargs),
                             save=True)
        article.save()
        newpath = cls.objects.create(
            site=site,
            parent=parent,
            slug=slug,
            article=article)
        article.add_object_relation(newpath)
        return newpath


######################################################
# SIGNAL HANDLERS
######################################################

# Just get this once
urlpath_content_type = None


@disable_signal_for_loaddata
def on_article_relation_save(**kwargs):
    global urlpath_content_type
    instance = kwargs['instance']
    if not urlpath_content_type:
        urlpath_content_type = ContentType.objects.get_for_model(URLPath)
    if instance.content_type == urlpath_content_type:
        URLPath.objects.filter(
            id=instance.object_id).update(
            article=instance.article)

post_save.connect(on_article_relation_save, ArticleForObject)


class Namespace:
    # An instance of Namespace simulates "nonlocal variable_name" declaration
    # in any nested function, that is possible in Python 3. It allows assigning
    # to non local variable without rebinding it local. See PEP 3104.
    pass


def on_article_delete(instance, *args, **kwargs):
    # If an article is deleted, then throw out its URLPaths
    # But move all descendants to a lost-and-found node.
    site = Site.objects.get_current()

    # Get the Lost-and-found path or create a new one
    # Only create the lost-and-found article if it's necessary and such
    # that the lost-and-found article can be deleted without being recreated!
    ns = Namespace()   # nonlocal namespace backported to Python 2.x
    ns.lost_and_found = None

    def get_lost_and_found():
        if ns.lost_and_found:
            return ns.lost_and_found
        try:
            ns.lost_and_found = URLPath.objects.get(
                slug=settings.LOST_AND_FOUND_SLUG,
                parent=URLPath.root(),
                site=site)
        except URLPath.DoesNotExist:
            article = Article(group_read=True,
                              group_write=False,
                              other_read=False,
                              other_write=False)
            article.add_revision(
                ArticleRevision(
                    content=_(
                        'Articles who lost their parents\n'
                        '===============================\n\n'
                        'The children of this article have had their parents deleted. You should probably find a new home for them.'),
                    title=_("Lost and found")))
            ns.lost_and_found = URLPath.objects.create(
                slug=settings.LOST_AND_FOUND_SLUG,
                parent=URLPath.root(),
                site=site,
                article=article)
            article.add_object_relation(ns.lost_and_found)
        return ns.lost_and_found

    for urlpath in URLPath.objects.filter(
            articles__article=instance,
            site=site):
        # Delete the children
        for child in urlpath.get_children():
            child.move_to(get_lost_and_found())
        # ...and finally delete the path itself

pre_delete.connect(on_article_delete, Article)
