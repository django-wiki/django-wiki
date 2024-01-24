from django import template
from wiki.plugins.pymdown import settings

register = template.Library()


@register.simple_tag
def allowed_pymdown_macros():
    for method in settings.pymdown_docs:
        yield method
