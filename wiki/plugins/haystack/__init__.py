from __future__ import absolute_import
from __future__ import unicode_literals
from wiki.conf import settings
from wiki.core import permissions
from wiki import models

from haystack import views as haystack_views
from django.db.models import Q
from django.utils.decorators import classonlymethod
from django.shortcuts import redirect


class SearchViewHaystack(haystack_views.SearchView):
    results_per_page = 25
    template = "search/search.html"

    def __name__(self):  # @ReservedAssignment
        return "SearchViewHaystack"

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        return haystack_views.search_view_factory(
            view_class=cls,
            *
            args,
            **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # Do not allow anonymous users to search if they cannot read content
        if request.user.is_anonymous() and not settings.ANONYMOUS:
            return redirect(settings.LOGIN_URL)
        return super(
            SearchViewHaystack,
            self).dispatch(
            request,
            *args,
            **kwargs)

    def __filter_can_read(self, user):
        """Filter objects so only the ones with a user's reading access
         are included"""
        if user.has_perm('wiki.moderator'):
            return self.results
        if user.is_anonymous():
            q = self.results.filter(other_read='True')
            return q
        else:
            q = self.results.filter(
                Q(other_read=True) |
                Q(owner=user) |
                (Q(group__user=user) & Q(group_read=True))
            )
        return q

    def __call__(self, request):
        self.request = request
        if self.request.user.is_anonymous and not settings.ANONYMOUS:
            return redirect(settings.LOGIN_URL)

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()
        if not permissions.can_moderate(
                models.URLPath.root().article,
                self.request.user):
            self.results = self.__filter_can_read(self.request.user)
            #self.results = self.results.filter(current_revision__deleted=False)

        return self.create_response()

    def extra_context(self):
        extra = super(SearchViewHaystack, self).extra_context()
        extra['search_query'] = self.query
        return extra
