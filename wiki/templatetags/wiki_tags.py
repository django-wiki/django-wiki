from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.forms import BaseForm
register = template.Library()

from wiki import models

@register.inclusion_tag('wiki/article/render.html')
def wiki_article(obj):
    
    if not isinstance(obj, Model):
        raise TypeError("A Wiki article can only be associated to a Django Model instance, not %s" % type(obj))
    
    content_type = ContentType.objects.get_for_model(obj)
    try:
        article = models.ArticleForObject.objects.get(content_type=content_type, object_id=obj.pk).article
    except models.ArticleForObject.DoesNotExist:
        article = None
    
    return {
        'obj': obj,
        'article': article,
    }

@register.inclusion_tag('wiki/includes/form.html', takes_context=True)
def wiki_form(context, form_obj):
    
    if not isinstance(form_obj, BaseForm):
        raise TypeError("Error including form, it's not a form, it's a %s" % type(form_obj))
    
    return {
        'form': form_obj,
    }
