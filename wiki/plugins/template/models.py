# -*- coding: utf-8 -*-
# This models.py is modified from the wiki.plugins.attachments.models.

from __future__ import print_function, unicode_literals

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from . import settings

from wiki import managers
from wiki.models.pluginbase import ReusablePlugin
from wiki.models.article import BaseRevisionMixin
from wiki.core.markdown import article_markdown


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
    extend_to_children = models.BooleanField(
        verbose_name=_('extend'),
        default=False,
        help_text=_(
            'You can extent this template to children articles.'
            'They will be able to use this template without import.'
        ),
    )

    def can_write(self, user):
        if not settings.ANONYMOUS_WRITE and (not user or user.is_anonymous()):
            return False
        return self.article.can_write(user)
        # return ReusablePlugin.can_write(self, user)

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

    @classmethod
    def get_by_article(cls, article):
        from django.db.models import Q
        articles = []
        urlapth = article.urlpath_set.all()
        if not urlapth:
            return cls.objects.none()
        else:
            urlapth = urlapth[0]
        while urlapth.parent:
            articles.append(urlapth.parent.article.id)
            urlapth = urlapth.parent
        return cls.objects.filter(
            Q(current_revision__deleted=False),
            Q(articles=article) | (
                Q(article__in=articles) & Q(extend_to_children=True))
        )

    def render(self, preview_content=None):
        if not self.current_revision:
            return ""
        if preview_content:
            content = preview_content
        else:
            content = self.current_revision.template_content
        return mark_safe(article_markdown(content, self))

    @property
    def md_tag(self):
        return "{{%(title)s%(vals)s}}" % {
            "title": self.template_title,
            "vals": self.md_vals,
        }

    @property
    def md_vals(self):
        from functools import reduce
        from six import text_type
        content = self.current_revision.template_content
        vals = []
        RE_TEXT = r'.*{{{(.*?)}}}.*'
        for li in content.splitlines():
            while re.search(RE_TEXT, li):
                sss = re.sub(RE_TEXT, r"\1", li)
                li = li.replace("{{{%s}}}" % sss, "")
                vals.append(sss)
        vals.sort()
        number_val = map(int, filter(lambda x: x.isdigit(), vals))
        if number_val:
            max_num_val = reduce(lambda x, y: max(x, y), number_val)
            num_vals = "|" + \
                "|".join(map(lambda x: text_type(x), range(max_num_val+1)))
        else:
            num_vals = ""
        named_val = filter(lambda x: not x.isdigit(), vals)
        named_val = "|".join(map(lambda x: x+"=", named_val))
        named_val = "|"+named_val if named_val else ""
        return "%(num_vals)s%(named_val)s" % {
            "num_vals": num_vals,
            "named_val": named_val,
        }

    @property
    def no_empty_description(self):
        template_desc_qs = self.templaterevision_set.exclude(description='').order_by("-revision_number")
        return template_desc_qs[0].description if template_desc_qs else ''


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

        # Clear article cache
        for article in self.template.articles.all():
            article.clear_cache()

    def __unicode__(self):
        return "%s: %s (r%d)" % (self.template.article.current_revision.title,
                                 self.template.template_title,
                                 self.revision_number)

    def render(self):
        return mark_safe(article_markdown(self.content, self.template))
