from __future__ import absolute_import, unicode_literals

from django import template
from wiki.plugins.images import models, settings

register = template.Library()


@register.filter
def images_for_article(article):
    return models.Image.objects.filter(
        article=article, current_revision__deleted=False).order_by(
        '-current_revision__created')


@register.filter
def images_can_add(article, user):
    if not settings.ANONYMOUS and (not user or user.is_anonymous()):
        return False
    return article.can_write(user)
