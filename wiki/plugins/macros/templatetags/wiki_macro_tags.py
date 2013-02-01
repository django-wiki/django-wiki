from django import template

register = template.Library()


@register.inclusion_tag(
    'wiki/plugins/templatetags/article_list.html',
    takes_context=True
)
def article_list(context, urlpath, depth):
    context['parent'] = urlpath 
    context['depth'] = depth 
    return context 


