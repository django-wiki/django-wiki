# -*- coding: utf-8 -*-
# This models.py is modified from the wiki.plugins.attachments.models.

from __future__ import print_function, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from . import settings

from wiki import managers
from wiki.models.pluginbase import ReusablePlugin
from wiki.models.article import BaseRevisionMixin
from wiki.core import article_markdown


class Template(ReusablePlugin):

    objects = managers.ArticleFkManager()

    current_revision = models.OneToOneField(
        'TemplateRevision',
        verbose_name=_('current revision'),
        blank=True, null=True, related_name='current_set',
        help_text=_(
            'The revision of this template currently in use (on all articles using the template)'),
    )

    template_title = models.SlugField(unique=True)

    def can_write(self, user):
        if not settings.ANONYMOUS_WRITE and (not user or user.is_anonymous()):
            return False
        return ReusablePlugin.can_write(self, user)

    def can_read(self, user):
        return settings.ANONYMOUS

    def can_moderate(self, user):
        return self.can_write(user)

    def can_delete(self, user):
        return self.can_write(user)

    class Meta:
        verbose_name = _('template')
        verbose_name_plural = _('templates')
        if settings.APP_LABEL:
            app_label = settings.APP_LABEL

    def __unicode__(self):
        return "%s Template: %s" % (self.article.current_revision.title, self.template_title)

    def render(self, preview_content=None):
        if not self.current_revision:
            return ""
        if preview_content:
            content = preview_content
        else:
            content = self.current_revision.template_content
        return mark_safe(article_markdown(content, self))


class TemplateRevision(BaseRevisionMixin, models.Model):

    template = models.ForeignKey('Template')
    template_content = models.TextField(
        verbose_name=_('template content'),
        blank=True,
        help_text=_("Does not support nested template."),
    )

    description = models.TextField(verbose_name=_('description'), blank=True)

    class Meta:
        verbose_name = _('template revision')
        verbose_name_plural = _('template revisions')
        ordering = ('created',)
        get_latest_by = 'revision_number'
        if settings.APP_LABEL:
            app_label = settings.APP_LABEL

    def save(self, *args, **kwargs):
        if (not self.id and
                not self.previous_revision and
                self.template and
                self.template.current_revision and
                self.template.current_revision != self):

            self.previous_revision = self.template.current_revision

        if not self.revision_number:
            try:
                previous_revision = self.template.templaterevision_set.latest()
                self.revision_number = previous_revision.revision_number + 1
            # NB! The above should not raise the below exception, but somehow it
            # does.
            except TemplateRevision.DoesNotExist as noattach:
                Template.DoesNotExist = noattach
                self.revision_number = 1

        super(TemplateRevision, self).save(*args, **kwargs)

        if not self.template.current_revision:
            # If I'm saved from Django admin, then template.current_revision is
            # me!
            self.template.current_revision = self
            self.template.save()

    def __unicode__(self):
        return "%s: %s (r%d)" % (self.template.article.current_revision.title,
                                 self.template.template_title,
                                 self.revision_number)

    def render(self):
        return mark_safe(article_markdown(self.content, self.template))
