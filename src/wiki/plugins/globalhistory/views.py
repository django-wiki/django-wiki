from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from wiki import models
from wiki.core.paginator import WikiPaginator


class GlobalHistory(ListView):

    template_name = 'wiki/plugins/globalhistory/globalhistory.html'
    paginator_class = WikiPaginator
    paginate_by = 30
    model = models.ArticleRevision
    context_object_name = 'revisions'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.only_last = kwargs.get('only_last', 0)
        return super(GlobalHistory, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        if self.only_last == '1':
            return self.model.objects.can_read(self.request.user) \
                .filter(article__current_revision=F('id')).order_by('-modified')
        else:
            return self.model.objects.can_read(self.request.user).order_by('-modified')

    def get_context_data(self, **kwargs):
        kwargs['only_last'] = self.only_last
        return super(GlobalHistory, self).get_context_data(**kwargs)
