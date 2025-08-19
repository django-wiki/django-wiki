from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import FormView

from . import forms
from . import models


class NotificationSettings(FormView):
    template_name = "wiki/plugins/notifications/settings.html"
    form_class = forms.SettingsFormSet

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, formset):
        for form in formset:
            settings = form.save()
            messages.info(
                self.request,
                _(
                    "You will receive notifications %(interval)s for "
                    "%(articles)d articles"
                )
                % {
                    "interval": settings.get_interval_display(),
                    "articles": self.get_article_subscriptions(
                        form.instance
                    ).count(),
                },
            )
        return redirect("wiki:notification_settings")

    def get_article_subscriptions(self, nyt_settings):
        return (
            models.ArticleSubscription.objects.filter(
                subscription__settings=nyt_settings,
                article__current_revision__deleted=False,
            )
            .select_related("article", "article__current_revision")
            .distinct()
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["form_kwargs"] = {"user": self.request.user}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = context["form"]
        for form in context["formset"]:
            if form.instance:
                form.instance.articlesubscriptions = (
                    self.get_article_subscriptions(form.instance)
                )
        return context
