from __future__ import unicode_literals
from django import forms
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.utils.translation import ugettext as _

from django_nyt.models import Settings, NotificationType
from django_nyt import settings as notify_settings
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

from wiki.plugins.notifications.settings import ARTICLE_EDIT
from wiki.core.plugins.base import PluginSettingsFormMixin

from wiki.plugins.notifications import models


class SettingsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return _("Receive notifications %s") % (obj.get_interval_display(), )


class ArticleSubscriptionModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return _("%(title)s - %(url)s" % {'title': obj.article.current_revision.title,
                      'url': obj.article.get_absolute_url()})


class SettingsModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SettingsModelForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        self.__editing_instance = False
        if instance:
            self.__editing_instance = True
            self.fields['delete_subscriptions'] = ArticleSubscriptionModelMultipleChoiceField(
                models.ArticleSubscription.objects.filter(settings=instance),
                label=_("Remove subscriptions"),
                required=False,
                help_text=_("Select article subscriptions to remove from notifications"),
                initial=models.ArticleSubscription.objects.none(),
            )
            self.fields['email'] = forms.TypedChoiceField(
                label=_("Email digests"),
                choices=(
                    (0, _('Unchanged (selected on each article)')),
                    (1, _('No emails')),
                    (2, _('Email on any change')),
                ),
                coerce=lambda x: int(x) if x else None,
                widget=forms.RadioSelect(),
                required=False,
                initial=0,
            )

    def save(self, *args, **kwargs):
        instance = super(SettingsModelForm, self).save(*args, **kwargs)
        if self.__editing_instance:
            # Django < 1.5 returns list objects when ModelMultipleChoiceField
            # is empty.. so check before calling delete()
            if self.cleaned_data['delete_subscriptions']:
                self.cleaned_data['delete_subscriptions'].delete()
            if self.cleaned_data['email'] == 1:
                instance.subscription_set.all().update(
                    send_emails=False,
                )
            if self.cleaned_data['email'] == 2:
                instance.subscription_set.all().update(
                    send_emails=True,
                )
        return instance


class BaseSettingsFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BaseSettingsFormSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return Settings.objects.filter(
            user=self.user,
            subscription__articlesubscription__article__current_revision__deleted=False,
        ).prefetch_related('subscription_set__articlesubscription',)


SettingsFormSet = modelformset_factory(
    Settings,
    form=SettingsModelForm,
    formset=BaseSettingsFormSet,
    extra=0,
    fields=('interval', ),
)


class SubscriptionForm(PluginSettingsFormMixin, forms.Form):

    settings_form_headline = _('Notifications')
    settings_order = 1
    settings_write_access = False

    settings = SettingsModelChoiceField(
        Settings,
        empty_label=None,
        label=_('Settings')
    )
    edit = forms.BooleanField(
        required=False,
        label=_('When this article is edited')
    )
    edit_email = forms.BooleanField(
        required=False,
        label=_('Also receive emails about article edits'),
        widget=forms.CheckboxInput(
            attrs={'onclick': mark_safe("$('#id_edit').attr('checked', $(this).is(':checked'));")}
        )
    )

    def __init__(self, article, request, *args, **kwargs):

        self.article = article
        self.user = request.user
        initial = kwargs.pop('initial', None)
        self.notification_type = NotificationType.objects.get_or_create(
            key=ARTICLE_EDIT,
            content_type=ContentType.objects.get_for_model(article)
        )[0]
        self.edit_notifications = models.ArticleSubscription.objects.filter(
            article=article,
            notification_type=self.notification_type
        )
        self.default_settings = Settings.objects.get_or_create(
            user=request.user,
            interval=notify_settings.INTERVALS_DEFAULT
        )[0]
        if self.edit_notifications:
            self.default_settings = self.edit_notifications[0].settings
        if not initial:
            initial = {
                'edit': bool(self.edit_notifications),
                'edit_email': bool(self.edit_notifications.filter(send_emails=True)),
                'settings': self.default_settings,
            }
        kwargs['initial'] = initial
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['settings'].queryset = Settings.objects.filter(
            user=request.user,
        )

    def get_usermessage(self):
        if self.changed_data:
            return _('Your notification settings were updated.')
        else:
            return _('Your notification settings were unchanged, so nothing saved.')

    def save(self, *args, **kwargs):

        cd = self.cleaned_data
        if not self.changed_data:
            return
        if cd['edit']:
            edit_notification = models.ArticleSubscription.objects.get_or_create(
                article=self.article,
                notification_type=self.notification_type,
                settings=cd['settings'],
            )[0]
            edit_notification.settings = cd['settings']
            edit_notification.send_emails = cd['edit_email']
            edit_notification.save()
        else:
            self.edit_notifications.delete()
