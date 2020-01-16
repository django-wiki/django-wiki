from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.models import BaseModelFormSet, modelformset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy as _
from django_nyt.models import NotificationType, Settings, Subscription
from wiki.core.plugins.base import PluginSettingsFormMixin
from wiki.plugins.notifications import models
from wiki.plugins.notifications.settings import ARTICLE_EDIT


class SettingsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return gettext("Receive notifications %(interval)s") % {
            "interval": obj.get_interval_display()
        }


class ArticleSubscriptionModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return gettext("%(title)s - %(url)s") % {
            "title": obj.article.current_revision.title,
            "url": obj.article.get_absolute_url(),
        }


class SettingsModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        self.__editing_instance = False
        if instance:
            self.__editing_instance = True
            self.fields[
                "delete_subscriptions"
            ] = ArticleSubscriptionModelMultipleChoiceField(
                models.ArticleSubscription.objects.filter(
                    subscription__settings=instance,
                    article__current_revision__deleted=False,
                ),
                label=gettext("Remove subscriptions"),
                required=False,
                help_text=gettext(
                    "Select article subscriptions to remove from notifications"
                ),
                initial=models.ArticleSubscription.objects.none(),
            )
            self.fields["email"] = forms.TypedChoiceField(
                label=_("Email digests"),
                choices=(
                    (0, gettext("Unchanged (selected on each article)")),
                    (1, gettext("No emails")),
                    (2, gettext("Email on any change")),
                ),
                coerce=lambda x: int(x) if x is not None else None,
                widget=forms.RadioSelect(),
                required=False,
                initial=0,
            )

    def save(self, *args, **kwargs):
        instance = super().save(*args, commit=False, **kwargs)
        instance.user = self.user
        if self.__editing_instance:
            self.cleaned_data["delete_subscriptions"].delete()
            if self.cleaned_data["email"] == 1:
                instance.subscription_set.all().update(send_emails=False,)
            elif self.cleaned_data["email"] == 2:
                instance.subscription_set.all().update(send_emails=True,)
        instance.save()
        return instance


class BaseSettingsFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")

        # Ensure that at least 1 default settings object exists
        all_settings = Settings.objects.filter(user=self.user).order_by("is_default")
        if not all_settings.exists():
            Settings.objects.create(user=self.user, is_default=True)
        else:
            to_update = all_settings.first()
            if not to_update.is_default:
                to_update.is_default = True
                to_update.save()
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return (
            Settings.objects.filter(user=self.user,)
            .exclude(
                subscription__articlesubscription__article__current_revision__deleted=True,
            )
            .prefetch_related("subscription_set__articlesubscription",)
            .order_by("is_default")
            .distinct()
        )


SettingsFormSet = modelformset_factory(
    Settings,
    form=SettingsModelForm,
    formset=BaseSettingsFormSet,
    extra=0,
    fields=("interval",),
)


class SubscriptionForm(PluginSettingsFormMixin, forms.Form):

    settings_form_headline = _("Notifications")
    settings_order = 1
    settings_write_access = False

    settings = SettingsModelChoiceField(None, empty_label=None, label=_("Settings"))
    edit = forms.BooleanField(required=False, label=_("When this article is edited"))
    edit_email = forms.BooleanField(
        required=False,
        label=_("Also receive emails about article edits"),
        widget=forms.CheckboxInput(
            attrs={
                "onclick": mark_safe(
                    "$('#id_edit').attr('checked', $(this).is(':checked'));"
                )
            }
        ),
    )

    def __init__(self, article, request, *args, **kwargs):
        self.article = article
        self.user = request.user
        initial = kwargs.pop("initial", None)
        self.notification_type = NotificationType.objects.get_or_create(
            key=ARTICLE_EDIT, content_type=ContentType.objects.get_for_model(article)
        )[0]
        self.edit_notifications = models.ArticleSubscription.objects.filter(
            article=article,
            subscription__notification_type=self.notification_type,
            subscription__settings__user=self.user,
        )
        self.default_settings = Settings.get_default_setting(request.user)
        if self.edit_notifications:
            self.default_settings = self.edit_notifications[0].subscription.settings
        if not initial:
            initial = {
                "edit": bool(self.edit_notifications),
                "edit_email": bool(
                    self.edit_notifications.filter(subscription__send_emails=True)
                ),
                "settings": self.default_settings,
            }
        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)
        self.fields["settings"].queryset = Settings.objects.filter(user=request.user,)

    def get_usermessage(self):
        if self.changed_data:
            return _("Your notification settings were updated.")
        else:
            return _("Your notification settings were unchanged, so nothing saved.")

    def save(self, *args, **kwargs):
        if not self.changed_data:
            return
        if self.cleaned_data["edit"]:
            try:
                edit_notification = models.ArticleSubscription.objects.get(
                    subscription__notification_type=self.notification_type,
                    article=self.article,
                    subscription__settings=self.cleaned_data["settings"],
                )
                edit_notification.subscription.send_emails = self.cleaned_data[
                    "edit_email"
                ]
                edit_notification.subscription.save()
            except models.ArticleSubscription.DoesNotExist:
                subscription, __ = Subscription.objects.get_or_create(
                    settings=self.cleaned_data["settings"],
                    notification_type=self.notification_type,
                    object_id=self.article.id,
                )
                models.ArticleSubscription.objects.create(
                    subscription=subscription, article=self.article,
                )
                subscription.send_emails = self.cleaned_data["edit_email"]
                subscription.save()

        else:
            self.edit_notifications.delete()
