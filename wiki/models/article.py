# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from wiki.conf import settings
from wiki.core import article_markdown, permissions
from wiki.core.plugins import registry as plugin_registry
from wiki import managers
from mptt.models import MPTTModel

class Article(models.Model):
    
    objects = managers.ArticleManager()
    
    current_revision = models.OneToOneField('ArticleRevision', 
                                            verbose_name=_(u'current revision'),
                                            blank=True, null=True, related_name='current_set',
                                            help_text=_(u'The revision being displayed for this article. If you need to do a roll-back, simply change the value of this field.'),
                                            )
    
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u'created'),)
    modified = models.DateTimeField(auto_now=True, verbose_name=_(u'modified'),
                                    help_text=_(u'Article properties last modified'))

    owner = models.ForeignKey(User, verbose_name=_('owner'),
                              blank=True, null=True, related_name='owned_articles',
                              help_text=_(u'The owner of the article, usually the creator. The owner always has both read and write access.'),)
    
    group = models.ForeignKey(Group, verbose_name=_('group'),
                              blank=True, null=True,
                              help_text=_(u'Like in a UNIX file system, permissions can be given to a user according to group membership. Groups are handled through the Django auth system.'),)
    
    group_read = models.BooleanField(default=True, verbose_name=_(u'group read access'))
    group_write = models.BooleanField(default=True, verbose_name=_(u'group write access'))
    other_read = models.BooleanField(default=True, verbose_name=_(u'others read access'))
    other_write = models.BooleanField(default=True, verbose_name=_(u'others write access'))
    
    # TODO: Do not use kwargs, it can lead to dangerous situations with bad
    # permission checking patterns. Also, since there are no other keywords,
    # it doesn't make much sense.
    def can_read(self, user=None):
        # Deny reading access to deleted articles if user has no delete access
        if self.current_revision and self.current_revision.deleted and not self.can_delete(user):
            return False
        
        # Check access for other users...
        if user.is_anonymous() and not settings.ANONYMOUS:
            return False
        elif self.other_read:
            return True
        elif user.is_anonymous():
            return  False
        if user == self.owner:
            return True
        if self.group_read:
            if self.group and user.groups.filter(id=self.group.id).exists():
                return True
        if self.can_moderate(user):
            return True
        return False
    
    def can_write(self, user=None):
        # Check access for other users...
        if user.is_anonymous() and not settings.ANONYMOUS_WRITE:
            return False
        elif self.other_write:
            return True
        elif user.is_anonymous():
            return  False
        if user == self.owner:
            return True
        if self.group_write:
            if self.group and user and user.groups.filter(id=self.group.id).exists():
                return True
        if self.can_moderate(user):
            return True
        return False
    
    def can_delete(self, user):
        return permissions.can_delete(self, user)
    def can_moderate(self, user):
        return permissions.can_moderate(self, user)
    def can_assign(self, user):
        return permissions.can_assign(self, user)
    
    def descendant_objects(self):
        """NB! This generator is expensive, so use it with care!!"""
        for obj in self.articleforobject_set.filter(is_mptt=True):
            for descendant in obj.content_object.get_descendants():
                yield descendant
    
    def get_children(self, max_num=None, user_can_read=None, **kwargs):
        """NB! This generator is expensive, so use it with care!!"""
        cnt = 0
        for obj in self.articleforobject_set.filter(is_mptt=True):
            if user_can_read:
                objects = obj.content_object.get_children().filter(**kwargs).can_read(user_can_read)
            else:
                objects = obj.content_object.get_children().filter(**kwargs)
            for child in objects.order_by('articles__article__current_revision__title'):
                cnt += 1
                if max_num and cnt > max_num: return
                yield child

    # All recursive permission methods will use descendant_objects to access
    # generic relations and check if they are using MPTT and have INHERIT_PERMISSIONS=True
    def set_permissions_recursive(self):
        for descendant in self.descendant_objects():
            if descendant.INHERIT_PERMISSIONS:
                descendant.group_read = self.group_read
                descendant.group_write = self.group_write
                descendant.other_read = self.other_read
                descendant.other_write = self.other_write
                descendant.save()
    
    def set_group_recursive(self):
        for descendant in self.descendant_objects():
            if descendant.INHERIT_PERMISSIONS:
                descendant.group = self.group
                descendant.save()

    def set_owner_recursive(self):
        for descendant in self.descendant_objects():
            if descendant.INHERIT_PERMISSIONS:
                descendant.owner = self.owner
                descendant.save()
    
    def add_revision(self, new_revision, save=True):
        """
        Sets the properties of a revision and ensures its the current
        revision.
        """
        assert self.id or save, ('Article.add_revision: Sorry, you cannot add a' 
                                 'revision to an article that has not been saved '
                                 'without using save=True')
        if not self.id: self.save()
        revisions = self.articlerevision_set.all()
        try:
            new_revision.revision_number = revisions.latest().revision_number + 1
        except ArticleRevision.DoesNotExist:
            new_revision.revision_number = 0
        new_revision.article = self
        new_revision.previous_revision = self.current_revision
        if save: new_revision.save()
        self.current_revision = new_revision
        if save: self.save()
    
    def add_object_relation(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        is_mptt = isinstance(obj, MPTTModel)
        rel = ArticleForObject.objects.get_or_create(article=self,
                                                     content_type=content_type,
                                                     object_id=obj.id,
                                                     is_mptt=is_mptt)
        return rel
    
    @classmethod
    def get_for_object(cls, obj):
        return ArticleForObject.objects.get(object_id=obj.id, content_type=ContentType.objects.get_for_model(obj)).article
    
    def __unicode__(self):
        if self.current_revision:
            return self.current_revision.title
        return _(u'Article without content (%(id)d)') % {'id': self.id}
    
    class Meta:
        app_label = settings.APP_LABEL
        permissions = (
            ("moderate", "Can edit all articles and lock/unlock/restore"),
            ("assign", "Can change ownership of any article"),
            ("grant", "Can assign permissions to other users"),
        )
    
    def render(self, preview_content=None):
        if not self.current_revision:
            return ""
        if preview_content:
            content = preview_content
        else:
            content = self.current_revision.content
        extensions = plugin_registry.get_markdown_extensions()
        extensions += settings.MARKDOWN_EXTENSIONS
        return mark_safe(article_markdown(content, self, extensions=extensions))
        
    
class ArticleForObject(models.Model):
    
    objects = managers.ArticleFkManager()
    
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    # Same as django.contrib.comments
    content_type   = models.ForeignKey(ContentType,
                                       verbose_name=_('content type'),
                                       related_name="content_type_set_for_%(class)s")
    object_id      = models.PositiveIntegerField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    is_mptt = models.BooleanField(default=False, editable=False)
    
    class Meta:
        app_label = settings.APP_LABEL
        verbose_name = _(u'Article for object')
        verbose_name_plural = _(u'Articles for object')
        # Do not allow several objects
        unique_together = ('content_type', 'object_id')

class BaseRevisionMixin(models.Model):
    """This is an abstract model used as a mixin: Do not override any of the 
    core model methods but respect the inheritor's freedom to do so itself."""
    
    revision_number = models.IntegerField(editable=False, verbose_name=_(u'revision number'))

    user_message = models.TextField(blank=True,)
    automatic_log = models.TextField(blank=True, editable=False,)
    
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True, editable=False)
    user        = models.ForeignKey(User, verbose_name=_('user'),
                                    blank=True, null=True)    
    
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    previous_revision = models.ForeignKey('self', blank=True, null=True)
    
    # NOTE! The semantics of these fields are not related to the revision itself
    # but the actual related object. If the latest revision says "deleted=True" then
    # the related object should be regarded as deleted.
    deleted = models.BooleanField(verbose_name=_(u'deleted'))
    locked  = models.BooleanField(verbose_name=_(u'locked'))

    def set_from_request(self, request):
        if request.user.is_authenticated():
            self.user = request.user
            if settings.LOG_IPS_USERS:
                self.ip_address = request.META.get('REMOTE_ADDR', None)
        elif settings.LOG_IPS_ANONYMOUS:
            self.ip_address = request.META.get('REMOTE_ADDR', None)
    
    class Meta:
        abstract = True
    
class ArticleRevision(BaseRevisionMixin, models.Model):
    """This is where main revision data is stored. To make it easier to
    copy, do NEVER create m2m relationships."""
    
    article = models.ForeignKey('Article', on_delete=models.CASCADE,
                                verbose_name=_(u'article'))
    
    # This is where the content goes, with whatever markup language is used
    content = models.TextField(blank=True, verbose_name=_(u'article contents'))
    
    # This title is automatically set from either the article's title or
    # the last used revision...
    title = models.CharField(max_length=512, verbose_name=_(u'article title'), 
                             null=False, blank=False, help_text=_(u'Each revision contains a title field that must be filled out, even if the title has not changed'))
    
    # TODO:
    # Allow a revision to redirect to another *article*. This 
    # way, we can redirects and still maintain old content.
    #redirect = models.ForeignKey('Article', null=True, blank=True,
    #                             verbose_name=_(u'redirect'),
    #                             help_text=_(u'If set, the article will redirect to the contents of another article.'),
    #                             related_name='redirect_set')
    
    def __unicode__(self):
        return "%s (%d)" % (self.title, self.revision_number)
    
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
    
    def save(self, *args, **kwargs):
        if (not self.id and
            not self.previous_revision and 
            self.article and
            self.article.current_revision and 
            self.article.current_revision != self):
            
            self.previous_revision = self.article.current_revision

        if not self.revision_number:
            try:
                previous_revision = self.article.articlerevision_set.latest()
                self.revision_number = previous_revision.revision_number + 1
            except ArticleRevision.DoesNotExist:
                self.revision_number = 1

        super(ArticleRevision, self).save(*args, **kwargs)
        
        if not self.article.current_revision:
            # If I'm saved from Django admin, then article.current_revision is me!
            self.article.current_revision = self
            self.article.save()
    
    class Meta:
        app_label = settings.APP_LABEL
        get_latest_by = ('revision_number',)
        ordering = ('created',)
        unique_together = ('article', 'revision_number')
    
