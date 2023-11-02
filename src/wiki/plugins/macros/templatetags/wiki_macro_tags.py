from django import template
from wiki.plugins.macros import settings
from wiki.plugins.macros.mdx.macro import MacroPattern

register = template.Library()


@register.inclusion_tag(
    "wiki/plugins/templatetags/article_list.html", takes_context=True
)
def article_list(context, urlpath, depth):
    context["parent"] = urlpath
    context["depth"] = depth
    return context


@register.simple_tag
def allowed_macros():
    for method in settings.METHODS:
        try:
            yield getattr(MacroPattern, method).meta
        except AttributeError:
            continue
