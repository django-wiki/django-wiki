from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import re

from django.conf import settings as django_settings
from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.forms import BaseForm
from django.utils.safestring import mark_safe
from django.template.defaultfilters import striptags
from django.utils.http import urlquote
from six.moves import filter

register = template.Library()

from wiki.conf import settings
from wiki import models
from wiki.core.plugins import registry as plugin_registry

# Cache for looking up objects for articles... article_for_object is
# called more than once per page in multiple template blocks.
_cache = {}


@register.assignment_tag(takes_context=True)
def article_for_object(context, obj):
    if not isinstance(obj, Model):
        raise TypeError(
            "A Wiki article can only be associated to a Django Model "
            "instance, not %s" % type(obj)
        )

    content_type = ContentType.objects.get_for_model(obj)

    # TODO: This is disabled for now, as it should only fire once per request
    # Maybe store cache in the request object?
    if True or not obj in list(_cache.keys()):
        try:
            article = models.ArticleForObject.objects.get(
                content_type=content_type,
                object_id=obj.pk).article
        except models.ArticleForObject.DoesNotExist:
            article = None
        _cache[obj] = article
    return _cache[obj]


@register.inclusion_tag('wiki/includes/render.html', takes_context=True)
def wiki_render(context, article, preview_content=None):

    if preview_content:
        content = article.render(preview_content=preview_content)
    else:
        content = None
    context.update({
        'article': article,
        'content': content,
        'preview': not preview_content is None,
        'plugins': plugin_registry.get_plugins(),
        'STATIC_URL': django_settings.STATIC_URL,
        'CACHE_TIMEOUT': settings.CACHE_TIMEOUT,
    })
    return context


@register.inclusion_tag('wiki/includes/form.html', takes_context=True)
def wiki_form(context, form_obj):
    if not isinstance(form_obj, BaseForm):
        raise TypeError(
            "Error including form, it's not a form, it's a %s" %
            type(form_obj))
    context.update({'form': form_obj})
    return context


@register.filter
def get_content_snippet(content, keyword, max_words=30):
    max_words = int(max_words)
    p = re.compile(
        r'(?P<before>.*)%s(?P<after>.*)' %
        re.escape(keyword),
        re.MULTILINE | re.IGNORECASE | re.DOTALL)
    m = p.search(content)
    html = ""
    if m:
        words = list(filter(
            lambda x: x != "",
            striptags(
                m.group("before")).replace(
                "\n",
                " ").split(" ")))
        before_words = words[-max_words // 2:]
        words = list(filter(
            lambda x: x != "",
            striptags(
                m.group("after")).replace(
                "\n",
                " ").split(" ")))
        after = " ".join(words[:max_words - len(before_words)])
        before = " ".join(before_words)
        html = "%s %s %s" % (before, striptags(keyword), after)
        kw_p = re.compile(r'(%s)' % keyword, re.IGNORECASE)
        html = kw_p.sub(r"<strong>\1</strong>", html)
        html = mark_safe(html)
    else:
        html = " ".join(
            list(filter(
                lambda x: x != "",
                striptags(content).replace(
                    "\n",
                    " ").split(" ")))[
                :max_words])
    return html


@register.filter
def can_read(obj, user):
    """Articles and plugins have a can_read method..."""
    return obj.can_read(user)


@register.filter
def can_write(obj, user):
    """Articles and plugins have a can_write method..."""
    return obj.can_write(user)


@register.filter
def can_delete(obj, user):
    """Articles and plugins have a can_delete method..."""
    return obj.can_delete(user)


@register.filter
def can_moderate(obj, user):
    """Articles and plugins have a can_moderate method..."""
    return obj.can_moderate(user)


@register.filter
def is_locked(obj):
    """Articles and plugins have a can_delete method..."""
    return (obj.current_revision and obj.current_revision.locked)


@register.assignment_tag(takes_context=True)
def login_url(context):
    request = context['request']
    qs = request.META.get('QUERY_STRING', '')
    if qs:
        qs = urlquote('?' + qs)
    else:
        qs = ''
    return settings.LOGIN_URL + "?next=" + request.path + qs
