from __future__ import absolute_import, unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from wiki import models


class GlobalHistory(ListView):

    template_name = 'wiki/plugins/globalhistory/globalhistory.html'
    paginate_by = 30
    model = models.ArticleRevision
    context_object_name = 'revisions'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GlobalHistory, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.can_read(self.request.user).order_by('-modified')
