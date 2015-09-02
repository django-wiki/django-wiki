from __future__ import unicode_literals
from __future__ import absolute_import
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from .settings import RESULTS_PER_PAGE
from wiki import models


class GlobalHistory(TemplateView):

    template_name = 'wiki/plugins/globalhistory/globalhistory.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GlobalHistory, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GlobalHistory, self).get_context_data(**kwargs)

        # Since we display elements based on rights, we don't know the total
        # numbers of items nor the number of pages and we do 'manual'
        # pagination

        page = int(self.request.GET.get('page', 0))

        if page < 0:
            page = 0

        # Get offset based on page
        skip = page * RESULTS_PER_PAGE
        needed = (page + 1) * RESULTS_PER_PAGE

        current_pos = 0
        results = []
        # Get all modifications from database and fill results when
        # pos > skip and len(results) < needed

        for article_revision in models.ArticleRevision.objects.order_by('-modified'):

            if article_revision.article.can_read(self.request.user):

                if current_pos >= skip:
                    results.append(article_revision)

                current_pos += 1
                if len(results) >= needed:
                    break

        context['list'] = results
        context['page'] = page

        return context
