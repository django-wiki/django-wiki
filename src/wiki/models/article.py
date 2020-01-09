from django.conf import settings as django_settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.db.models.fields import GenericIPAddressField as IPAddressField
from django.db.models.signals import post_save, pre_delete, pre_save
from django.urls import reverse
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel
from wiki import managers
from wiki.conf import settings
from wiki.core import permissions
from wiki.core.markdown import article_markdown
from wiki.decorators import disable_signal_for_loaddata

__all__ = [
    "Article",
    "ArticleForObject",
    "ArticleRevision",
    "BaseRevisionMixin",
]


class Article(models.Model):

    objects = managers.ArticleManager()

    current_revision = models.OneToOneField(
        "ArticleRevision",
        verbose_name=_("current revision"),
        blank=True,
        null=True,
        related_name="current_set",
        on_delete=models.CASCADE,
        help_text=_(
            "The revision being displayed for this article. If you need to do a roll-back, simply change the value of this field."
        ),
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"),)
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_("modified"),
        help_text=_("Article properties last modified"),
    )

    owner = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        blank=True,
        null=True,
        related_name="owned_articles",
        help_text=_(
            "The owner of the article, usually the creator. The owner always has both read and write access."
        ),
        on_delete=models.SET_NULL,
    )

    group = models.ForeignKey(
        settings.GROUP_MODEL,
        verbose_name=_("group"),
        blank=True,
        null=True,
        help_text=_(
            "Like in a UNIX file system, permissions can be given to a user according to group membership. Groups are handled through the Django auth system."
        ),
        on_delete=models.SET_NULL,
    )

    group_read = models.BooleanField(default=True, verbose_name=_("group read access"))
    group_write = models.BooleanField(
        default=True, verbose_name=_("group write access")
    )
    other_read = models.BooleanField(default=True, verbose_name=_("others read access"))
    other_write = models.BooleanField(
        default=True, verbose_name=_("others write access")
    )

    # PERMISSIONS
    def can_read(self, user):
        return permissions.can_read(self, user)

    def can_write(self, user):
        return permissions.can_write(self, user)

    def can_delete(self, user):
        return permissions.can_delete(self, user)

    def can_moderate(self, user):
        return permissions.can_moderate(self, user)

    def can_assign(self, user):
        return permissions.can_assign(self, user)

    def ancestor_objects(self):
        """NB! This generator is expensive, so use it with care!!"""
        for obj in self.articleforobject_set.filter(is_mptt=True):
            yield from obj.content_object.get_ancestors()

    def descendant_objects(self):
        """NB! This generator is expensive, so use it with care!!"""
        for obj in self.articleforobject_set.filter(is_mptt=True):
            yield from obj.content_object.get_descendants()

    def get_children(self, max_num=None, user_can_read=None, **kwargs):
        """NB! This generator is expensive, so use it with care!!"""
        cnt = 0
        for obj in self.articleforobject_set.filter(is_mptt=True):
            if user_can_read:
                objects = (
                    obj.content_object.get_children()
                    .filter(**kwargs)
                    .can_read(user_can_read)
                )
            else:
                objects = obj.content_object.get_children().filter(**kwargs)
            for child in objects.order_by("articles__article__current_revision__title"):
                cnt += 1
                if max_num and cnt > max_num:
                    return
                yield child

    # All recursive permission methods will use descendant_objects to access
    # generic relations and check if they are using MPTT and have
    # INHERIT_PERMISSIONS=True
    def set_permissions_recursive(self):
        for descendant in self.descendant_objects():
            if descendant.INHERIT_PERMISSIONS:
                descendant.article.group_read = self.group_read
                descendant.article.group_write = self.group_write
                descendant.article.other_read = self.other_read
                descendant.article.other_write = self.other_write
                descendant.article.save()

    def set_group_recursive(self):
        for descendant in self.descendant_objects():
            if descendant.INHERIT_PERMISSIONS:
                descendant.article.group = self.group
                descendant.article.save()

    def set_owner_recursive(self):
        for descendant in self.descendant_objects():
            if descendant.INHERIT_PERMISSIONS:
                descendant.article.owner = self.owner
                descendant.article.save()

    def add_revision(self, new_revision, save=True):
        """
        Sets the properties of a revision and ensures its the current
        revision.
        """
        assert self.id or save, (
            "Article.add_revision: Sorry, you cannot add a"
            "revision to an article that has not been saved "
            "without using save=True"
        )
        if not self.id:
            self.save()
        revisions = self.articlerevision_set.all()
        try:
            new_revision.revision_number = revisions.latest().revision_number + 1
        except ArticleRevision.DoesNotExist:
            new_revision.revision_number = 0
        new_revision.article = self
        new_revision.previous_revision = self.current_revision
        if save:
            new_revision.clean()
            new_revision.save()
        self.current_revision = new_revision
        if save:
            self.save()

    def add_object_relation(self, obj):
        return ArticleForObject.objects.get_or_create(
            article=self,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
            is_mptt=isinstance(obj, MPTTModel),
        )

    @classmethod
    def get_for_object(cls, obj):
        return ArticleForObject.objects.get(
            object_id=obj.id, content_type=ContentType.objects.get_for_model(obj),
        ).article

    def __str__(self):
        if self.current_revision:
            return self.current_revision.title
        obj_name = _("Article without content (%(id)d)") % {"id": self.id}
        return str(obj_name)

    class Meta:
        permissions = (
            ("moderate", _("Can edit all articles and lock/unlock/restore")),
            ("assign", _("Can change ownership of any article")),
            ("grant", _("Can assign permissions to other users")),
        )

    def render(self, preview_content=None, user=None):
        if not self.current_revision:
            return ""
        if preview_content:
            content = preview_content
        else:
            content = self.current_revision.content
        return mark_safe(
            article_markdown(
                content, self, preview=preview_content is not None, user=user
            )
        )

    def get_cache_key(self):
        """Returns per-article cache key."""
        lang = translation.get_language()

        return "wiki:article:{id}:{lang}".format(
            id=self.current_revision.id if self.current_revision else self.id, lang=lang
        )

    def get_cache_content_key(self, user=None):
        """Returns per-article-user cache key."""
        return "{key}:{user}".format(
            key=self.get_cache_key(), user=user.get_username() if user else ""
        )

    def get_cached_content(self, user=None):
        """Returns cached version of rendered article.

        The cache contains one "per-article" entry plus multiple
        "per-article-user" entries. The per-article-user entries contain the
        rendered article, the per-article entry contains list of the
        per-article-user keys. The rendered article in cache (per-article-user)
        is used only if the key is in the per-article entry. To delete
        per-article invalidates all article cache entries."""

        cache_key = self.get_cache_key()
        cache_content_key = self.get_cache_content_key(user)

        cached_items = cache.get(cache_key, list())

        if cache_content_key in cached_items:
            cached_content = cache.get(cache_content_key)
            if cached_content is not None:
                return mark_safe(cached_content)

        cached_content = self.render(user=user)
        cached_items.append(cache_content_key)
        cache.set(cache_key, cached_items, settings.CACHE_TIMEOUT)
        cache.set(cache_content_key, cached_content, settings.CACHE_TIMEOUT)

        return mark_safe(cached_content)

    def clear_cache(self):
        cache.delete(self.get_cache_key())

    def get_url_kwargs(self):
        urlpaths = self.urlpath_set.all()
        if urlpaths.exists():
            return {"path": urlpaths[0].path}
        return {"article_id": self.id}

    def get_absolute_url(self):
        return reverse("wiki:get", kwargs=self.get_url_kwargs())


class ArticleForObject(models.Model):

    objects = managers.ArticleFkManager()

    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    # Same as django.contrib.comments
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("content type"),
        related_name="content_type_set_for_%(class)s",
    )
    object_id = models.PositiveIntegerField(_("object ID"))
    content_object = GenericForeignKey("content_type", "object_id")

    is_mptt = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return str(self.article)

    class Meta:
        verbose_name = _("Article for object")
        verbose_name_plural = _("Articles for object")
        # Do not allow several objects
        unique_together = ("content_type", "object_id")


class BaseRevisionMixin(models.Model):

    """This is an abstract model used as a mixin: Do not override any of the
    core model methods but respect the inheritor's freedom to do so itself."""

    revision_number = models.IntegerField(
        editable=False, verbose_name=_("revision number")
    )

    user_message = models.TextField(blank=True,)
    automatic_log = models.TextField(blank=True, editable=False,)

    ip_address = IPAddressField(_("IP address"), blank=True, null=True, editable=False)
    user = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    previous_revision = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.SET_NULL
    )

    # NOTE! The semantics of these fields are not related to the revision itself
    # but the actual related object. If the latest revision says "deleted=True" then
    # the related object should be regarded as deleted.
    deleted = models.BooleanField(verbose_name=_("deleted"), default=False,)
    locked = models.BooleanField(verbose_name=_("locked"), default=False,)

    def set_from_request(self, request):
        if request.user.is_authenticated:
            self.user = request.user
            if settings.LOG_IPS_USERS:
                self.ip_address = request.META.get("REMOTE_ADDR", None)
        elif settings.LOG_IPS_ANONYMOUS:
            self.ip_address = request.META.get("REMOTE_ADDR", None)

    def inherit_predecessor(self, predecessor):
        """
        This is a naive way of inheriting, assuming that ``predecessor`` is in
        fact the predecessor and there hasn't been any intermediate changes!

        :param: predecessor is an instance of whatever object for which
        object.current_revision implements BaseRevisionMixin.
        """
        predecessor = predecessor.current_revision
        self.previous_revision = predecessor
        self.deleted = predecessor.deleted
        self.locked = predecessor.locked
        self.revision_number = predecessor.revision_number + 1

    class Meta:
        abstract = True


class ArticleRevision(BaseRevisionMixin, models.Model):

    """This is where main revision data is stored. To make it easier to
    copy, do NEVER create m2m relationships."""

    objects = managers.ArticleFkManager()

    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, verbose_name=_("article")
    )

    # This is where the content goes, with whatever markup language is used
    content = models.TextField(blank=True, verbose_name=_("article contents"))

    # This title is automatically set from either the article's title or
    # the last used revision...
    title = models.CharField(
        max_length=512,
        verbose_name=_("article title"),
        null=False,
        blank=False,
        help_text=_(
            "Each revision contains a title field that must be filled out, even if the title has not changed"
        ),
    )

    # TODO:
    # Allow a revision to redirect to another *article*. This
    # way, we can have redirects and still maintain old content.
    # redirect = models.ForeignKey('Article', null=True, blank=True,
    #                             verbose_name=_('redirect'),
    #                             help_text=_('If set, the article will redirect to the contents of another article.'),
    #                             related_name='redirect_set')

    def __str__(self):
        return "%s (%d)" % (self.title, self.revision_number)

    def clean(self):
        # Enforce DOS line endings \r\n. It is the standard for web browsers,
        # but when revisions are created programatically, they might
        # have UNIX line endings \n instead.
        self.content = self.content.replace("\r", "").replace("\n", "\r\n")

    def inherit_predecessor(self, article):
        """
        Inherit certain properties from predecessor because it's very
        convenient. Remember to always call this method before
        setting properties :)"""
        predecessor = article.current_revision
        self.article = predecessor.article
        self.content = predecessor.content
        self.title = predecessor.title
        self.deleted = predecessor.deleted
        self.locked = predecessor.locked

    class Meta:
        get_latest_by = "revision_number"
        ordering = ("created",)
        unique_together = ("article", "revision_number")


######################################################
# SIGNAL HANDLERS
######################################################

# clear the ancestor cache when saving or deleting articles so things like
# article_lists will be refreshed
def _clear_ancestor_cache(article):
    for ancestor in article.ancestor_objects():
        ancestor.article.clear_cache()


@disable_signal_for_loaddata
def on_article_save_clear_cache(instance, **kwargs):
    on_article_delete_clear_cache(instance, **kwargs)


@disable_signal_for_loaddata
def on_article_delete_clear_cache(instance, **kwargs):
    _clear_ancestor_cache(instance)
    instance.clear_cache()


@disable_signal_for_loaddata
def on_article_revision_pre_save(**kwargs):
    instance = kwargs["instance"]
    if kwargs.get("created", False):
        revision_changed = (
            not instance.previous_revision
            and instance.article
            and instance.article.current_revision
            and instance.article.current_revision != instance
        )
        if revision_changed:
            instance.previous_revision = instance.article.current_revision

    if not instance.revision_number:
        try:
            previous_revision = instance.article.articlerevision_set.latest()
            instance.revision_number = previous_revision.revision_number + 1
        except ArticleRevision.DoesNotExist:
            instance.revision_number = 1


@disable_signal_for_loaddata
def on_article_revision_post_save(**kwargs):

    instance = kwargs["instance"]
    if not instance.article.current_revision:
        # If I'm saved from Django admin, then article.current_revision is
        # me!
        instance.article.current_revision = instance
        instance.article.save()


pre_save.connect(on_article_revision_pre_save, ArticleRevision)
post_save.connect(on_article_revision_post_save, ArticleRevision)
post_save.connect(on_article_save_clear_cache, Article)
pre_delete.connect(on_article_delete_clear_cache, Article)
