from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from wiki import models


class DeletedListView(TemplateView):

    template_name = "wiki/deleted_list.html"

    def dispatch(self, request, *args, **kwargs):
        # Let logged in super users continue
        if not request.user.is_superuser:
            return redirect('wiki:root')

        return super(DeletedListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        article_list = models.Article.objects.all()
        deleted_articles = []
        for article in article_list:
            if(article.current_revision.deleted):
                deleted_articles.append(article)
        kwargs['deleted_articles'] = deleted_articles
        context = super(DeletedListView, self).get_context_data(**kwargs)
        return context
