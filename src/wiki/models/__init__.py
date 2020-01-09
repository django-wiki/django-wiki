from django import shortcuts, urls
from django.urls import base
from django.utils.functional import lazy

from .article import *  # noqa
from .pluginbase import *  # noqa
from .urlpath import *  # noqa

original_django_reverse = urls.reverse


def reverse(*args, **kwargs):
    """Now this is a crazy and silly hack, but it is basically here to
    enforce that an empty path always takes precedence over an article_id
    such that the root article doesn't get resolved to /ID/ but /.

    Another crazy hack that this supports is transforming every wiki url
    by a function. If _transform_url is set on this function, it will
    return the result of calling reverse._transform_url(reversed_url)
    for every url in the wiki namespace.
    """
    if isinstance(args[0], str) and args[0].startswith("wiki:"):
        url_kwargs = kwargs.get("kwargs", {})
        path = url_kwargs.get("path", False)
        # If a path is supplied then discard the article_id
        if path is not False:
            url_kwargs.pop("article_id", None)
            url_kwargs["path"] = path
            kwargs["kwargs"] = url_kwargs

        url = original_django_reverse(*args, **kwargs)
        if hasattr(reverse, "_transform_url"):
            url = reverse._transform_url(url)
    else:
        url = original_django_reverse(*args, **kwargs)

    return url


reverse_lazy = lazy(reverse, str)


# Patch up other locations of the reverse function
base.reverse = reverse
base.reverse_lazy = reverse_lazy
urls.reverse = reverse
urls.reverse_lazy = reverse_lazy
shortcuts.reverse = reverse
