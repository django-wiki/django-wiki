from django.views.generic.base import TemplateView
from django.shortcuts import redirect

from wiki import models

class AdminPanelView(TemplateView):

    template_name = "wiki/admin_panel.html"

    def dispatch(self, request, *args, **kwargs):
        # Let logged in super users continue
        if not request.user.is_superuser:
            return redirect('wiki:root')

        return super(AdminPanelView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        articleList = models.Article.objects.all()
        deletedArticles = []
        for article in articleList:
            if(article.current_revision.deleted):
                deletedArticles.append(article)
        kwargs['deleted_articles'] = deletedArticles
        context = super(AdminPanelView, self).get_context_data(**kwargs)
        return context
