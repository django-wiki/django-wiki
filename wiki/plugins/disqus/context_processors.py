# -*- coding: utf-8 -*-

from .settings import DISQUS_SORTNAME

def disqus(request):
    context_extend = {}
    context_extend["WIKI_DISQUS_SORTNAME"] = DISQUS_SORTNAME
    context_extend["WIKI_DISQUS"] = DISQUS_SORTNAME or False
    return context_extend