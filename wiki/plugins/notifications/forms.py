from django import forms
from django.utils.translation import ugettext as _

from django_notify.models import Settings, NotificationType
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

from wiki.plugins.notifications import ARTICLE_EDIT
from wiki.core.plugins.base import PluginSettingsFormMixin

class SubscriptionForm(PluginSettingsFormMixin, forms.Form):
    
    settings_form_headline = _(u'Notifications')
    settings_order = 1
    settings_write_access = False
    
    edit = forms.BooleanField(required=False, label=_(u'When this article is edited'))
    edit_email = forms.BooleanField(required=False, label=_(u'Also receive emails about article edits'),
                                    widget=forms.CheckboxInput(attrs={'onclick': mark_safe("$('#id_edit').attr('checked', $(this).is(':checked'));")}))
    
    def __init__(self, article, request, *args, **kwargs):
        # This has to be here to avoid unresolved imports in wiki_plugins
        from wiki.plugins.notifications import models
        self.article = article
        self.user = request.user
        initial = kwargs.pop('initial', None)
        self.settings = Settings.objects.get_or_create(user=request.user,)[0]
        self.notification_type = NotificationType.objects.get_or_create(key=ARTICLE_EDIT,
                                                                        content_type=ContentType.objects.get_for_model(article))[0]
        self.edit_notifications=models.ArticleSubscription.objects.filter(settings=self.settings, 
                                                                          article=article,
                                                                          notification_type=self.notification_type)
        if not initial:
            initial = {'edit': bool(self.edit_notifications),
                       'edit_email': bool(self.edit_notifications.filter(send_emails=True))}
        kwargs['initial'] = initial
        super(SubscriptionForm, self).__init__(*args, **kwargs)
    
    def get_usermessage(self):
        if self.changed_data:
            return _('Your notification settings were updated.')
        else:
            return _('Your notification settings were unchanged, so nothing saved.')
    
    def save(self, *args, **kwargs):
        import models
        cd = self.cleaned_data
        if not self.changed_data:
            return
        if cd['edit']:
            edit_notification = models.ArticleSubscription.objects.get_or_create(settings=self.settings, 
                                                                                 article=self.article,
                                                                                 notification_type=self.notification_type)[0]
            edit_notification.send_emails = cd['edit_email']
            edit_notification.save()
        else:
            self.edit_notifications.delete()
