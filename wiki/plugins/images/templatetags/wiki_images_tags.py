from django import template

from wiki.plugins.images import models

register = template.Library()

@register.filter
def images_for_article(article):
    return models.Image.objects.filter(revision__article=article).order_by('-created')
