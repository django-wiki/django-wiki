# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.edit import FormView

import forms

class NotificationSettings(FormView):
    
    template_name = 'wiki/plugins/notifications/settings.html'
    form_class = forms.SettingsFormSet
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationSettings, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, formset):
        for form in formset:
            settings = form.save()
            import models
            article_subscriptions = models.ArticleSubscription.objects.filter(
                settings = form.instance,
                article__current_revision__deleted=False,
            ).select_related('article', 'article__current_revision')
            messages.info(
                self.request, 
                _(u"You will receive notifications %(interval)s for "
                   "%(articles)d articles") % 
                    {
                        'interval': settings.get_interval_display(),
                        'articles': article_subscriptions.count(),
                    }
            )
        return redirect('wiki:notification_settings')
    
    def get_form_kwargs(self):
        kwargs = FormView.get_form_kwargs(self)
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = FormView.get_context_data(self, **kwargs)
        context['formset'] = kwargs['form']
        import models
        for form in context['formset']:
            if form.instance:
                setattr(form.instance, 'articlesubscriptions', 
                    models.ArticleSubscription.objects.filter(
                        settings = form.instance,
                        article__current_revision__deleted=False,
                    ).select_related('article', 'article__current_revision')
                )
        return context
    