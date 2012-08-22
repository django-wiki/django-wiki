from django.conf import settings as django_settings
from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.forms import BaseForm

register = template.Library()

from wiki import models
from wiki.core.plugins import registry as plugin_registry

# Cache for looking up objects for articles... article_for_object is
# called more than once per page in multiple template blocks.
_cache = {}

@register.assignment_tag(takes_context=True)
def article_for_object(context, obj):
    if not isinstance(obj, Model):
        raise TypeError("A Wiki article can only be associated to a Django Model instance, not %s" % type(obj))
    
    content_type = ContentType.objects.get_for_model(obj)
    
    # TODO: This is disabled for now, as it should only fire once per request
    # Maybe store cache in the request object?
    if True or not obj in _cache.keys():
        try:
            article = models.ArticleForObject.objects.get(content_type=content_type, object_id=obj.pk).article
        except models.ArticleForObject.DoesNotExist:
            article = None
        _cache[obj] = article
    return _cache[obj]

@register.inclusion_tag('wiki/includes/render.html')
def wiki_render(article, preview_content=None):
    
    if preview_content:
        content = article.render(preview_content=preview_content)
    else:
        content = None
    return {
        'article': article,
        'content': content,
        'preview': not preview_content is None,
        'plugins': plugin_registry.get_plugins(),
        'STATIC_URL': django_settings.STATIC_URL,
    }

@register.inclusion_tag('wiki/includes/form.html', takes_context=True)
def wiki_form(context, form_obj):
    
    if not isinstance(form_obj, BaseForm):
        raise TypeError("Error including form, it's not a form, it's a %s" % type(form_obj))
    
    return {
        'form': form_obj,
    }

@register.filter
def can_read(obj, user):
    """Articles and plugins have a can_read method..."""
    return obj.can_read(user=user)

@register.filter
def can_write(obj, user):
    """Articles and plugins have a can_write method..."""
    return obj.can_write(user=user)

@register.filter
def can_delete(obj, user):
    """Articles and plugins have a can_delete method..."""
    return obj.can_delete(user)

@register.filter
def can_moderate(obj, user):
    """Articles and plugins have a can_moderate method..."""
    return obj.can_moderate(user)
