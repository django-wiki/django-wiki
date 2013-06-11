# Create your views here.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView

from django_notify import models

class NotificationSettings(ListView):
    
    template_name = 'wiki/plugins/notifications/settings.html'
    allow_empty = True
    context_object_name = 'settings'
    paginate_by = 10
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationSettings, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        settings = models.Settings.objects.filter(user=self.request.user)
        return settings
    