# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group

from wiki.conf import settings

class Article(models.Model):
    
    title = models.CharField(max_length=512, verbose_name=_(u'title'), 
                             null=False, blank=False)
    current_revision = models.ForeignKey('ArticleRevision', 
                                         verbose_name=_(u'current revision'),
                                         blank=True, null=True, related_name='current_set')
    
    owner = models.ForeignKey(User, verbose_name=_('owner'),
                              blank=True, null=True)
    
    group = models.ForeignKey(Group, verbose_name=_('group'),
                              blank=True, null=True)
    
    group_read = models.BooleanField(default=True)
    group_write = models.BooleanField(default=True)
    other_read = models.BooleanField(default=True)
    other_write = models.BooleanField(default=True)
    
    def can_read(self, user=None, group=None):
        if self.other_read:
            return True
        if user == self.owner:
            return True
        if self.group_read:
            if group == self.group:
                return True
            if self.group and user and user.groups.filter(group=group):
                return True
        return False
    
    def can_write(self, user=None, group=None):
        if self.other_write:
            return True
        if user == self.owner:
            return True
        if self.group_write:
            if group == self.group:
                return True
            if self.group and user and user.groups.filter(group=group):
                return True
        return False
    
    def decendant_objects(self):
        for obj in self.objectforarticle_set.filter(has_parent_field=True):
            for decendant in obj.get_decendants():
                yield decendant
    
    # All recursive permission methods will use decendant_objects to access
    # generic relations and check if they are using MPTT and have INHERIT_PERMISSIONS=True
    def set_permissions_recursive(self):
        for decendant in self.decendant_objects():
            if decendant.INHERIT_PERMISSIONS:
                decendant.group_read = self.group_read
                decendant.group_write = self.group_write
                decendant.other_read = self.other_read
                decendant.other_write = self.other_write
    
    def set_group_recursive(self):
        for decendant in self.decendant_objects():
            if decendant.INHERIT_PERMISSIONS:
                decendant.group = self.group

    def set_owner_recursive(self):
        for decendant in self.decendant_objects():
            if decendant.INHERIT_PERMISSIONS:
                decendant.owner = self.owner

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
        if save: new_revision.save()
        self.current_revision = new_revision
        if save: self.save()
    
    def add_object_relation(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        has_parent_field = hasattr(obj, 'parent')
        rel = ArticleForObject.objects.get_or_create(article=self,
                                                     content_type=content_type,
                                                     object_pk=obj.pk,
                                                     has_parent_method=has_parent_field)
        return rel
    
    @classmethod
    def get_for_object(cls, obj):
        return ArticleForObject.objects.get(object_id=obj.id, content_type=ContentType.objects.get_for_model(obj)).article
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        app_label = settings.APP_LABEL
    
class ArticleForObject(models.Model):
    article = models.ForeignKey('Article')    
    # Same as django.contrib.comments
    content_type   = models.ForeignKey(ContentType,
                                       verbose_name=_('content type'),
                                       related_name="content_type_set_for_%(class)s")
    object_id      = models.PositiveIntegerField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    has_parent_method = models.BooleanField(default=False, editable=False)
    
    class Meta:
        app_label = settings.APP_LABEL
        verbose_name = _(u'Article for object')
        verbose_name_plural = _(u'Articles for object')
        # Do not allow several objects
        unique_together = ('content_type', 'object_id')
    
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
                                 help_text=_(u'If set, the article will redirect to the contents of another article.'),
                                 related_name='redirect_set')
    
    # User details
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    user        = models.ForeignKey(User, verbose_name=_('user'),
                                    blank=True, null=True)
    
    # Various stuff
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = settings.APP_LABEL
        get_latest_by = ('id',)
    