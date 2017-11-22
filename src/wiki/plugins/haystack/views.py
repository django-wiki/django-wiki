from __future__ import unicode_literals

from haystack.backends import SQ
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet
from wiki import models
from wiki.core import permissions
from wiki.views.article import SearchView


class HaystackSearchView(SearchView):

    template_name = 'wiki/plugins/haystack/search.html'

    def get_queryset(self):
        qs = SearchQuerySet().all()
        if self.request.user.is_authenticated():
            if not permissions.can_moderate(
                    models.URLPath.root().article,
                    self.request.user):
                qs = qs.filter(
                    SQ(owner_id=self.request.user.id) |
                    (
                        SQ(group_id__in=self.request.user.groups.values_list('id', flat=True)) &
                        SQ(group_read=True)
                    ) |
                    SQ(other_read=True)
                )
        else:
            qs = qs.exclude(other_read=False)

        qs = qs.filter(content=AutoQuery(self.query))
        qs = qs.load_all()
        return qs
