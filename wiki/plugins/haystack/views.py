from wiki.views.article import SearchView
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
from wiki.core import permissions
from wiki import models

class HaystackSearchView(SearchView):
    
    template_name = 'wiki/plugins/haystack/search.html'
    
    def get_queryset(self):
        qs = SearchQuerySet().all()
        if self.request.user.is_authenticated():
            # TODO: This has a leak! It should say:
            # group=self.request.group.id AND group_read=True
            if not permissions.can_moderate(models.URLPath.root().article, 
                self.request.user):
                qs = qs.filter_or(
                    owner=self.request.user.id, 
                    group=self.request.group.id,
                    other_read=True
                )
        else:
            qs = qs.exclude(other_read=False)
        
        qs = qs.filter(content=AutoQuery(self.query))
        qs = qs.exclude(other_read=False)
        qs = qs.load_all()
        return qs
    