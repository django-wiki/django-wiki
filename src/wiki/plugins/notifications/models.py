from django.db import models
from django.db.models import signals
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_nyt.models import Subscription
from django_nyt.utils import notify
from wiki import models as wiki_models
from wiki.decorators import disable_signal_for_loaddata
from wiki.models.pluginbase import ArticlePlugin
from wiki.plugins.notifications import settings
from wiki.plugins.notifications.util import get_title


class ArticleSubscription(ArticlePlugin):

    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)

    def __str__(self):
        title = _("%(user)s subscribing to %(article)s (%(type)s)") % {
            "user": self.subscription.settings.user.username,
            "article": self.article.current_revision.title,
            "type": self.subscription.notification_type.label,
        }
        return str(title)

    class Meta:
        unique_together = ("subscription", "articleplugin_ptr")
        # Matches label of upcoming 0.1 release
        db_table = "wiki_notifications_articlesubscription"


def default_url(article, urlpath=None):
    if urlpath:
        return reverse("wiki:get", kwargs={"path": urlpath.path})
    return article.get_absolute_url()


@disable_signal_for_loaddata
def post_article_revision_save(**kwargs):
    instance = kwargs["instance"]
    if kwargs.get("created", False):
        url = default_url(instance.article)
        filter_exclude = {"settings__user": instance.user}
        if instance.deleted:
            notify(
                _("Article deleted: %s") % get_title(instance),
                settings.ARTICLE_EDIT,
                target_object=instance.article,
                url=url,
                filter_exclude=filter_exclude,
            )
        elif instance.previous_revision:
            notify(
                _("Article modified: %s") % get_title(instance),
                settings.ARTICLE_EDIT,
                target_object=instance.article,
                url=url,
                filter_exclude=filter_exclude,
            )
        else:
            notify(
                _("New article created: %s") % get_title(instance),
                settings.ARTICLE_EDIT,
                target_object=instance,
                url=url,
                filter_exclude=filter_exclude,
            )


# Whenever a new revision is created, we notifý users that an article
# was edited
signals.post_save.connect(
    post_article_revision_save,
    sender=wiki_models.ArticleRevision,
)

# TODO: We should notify users when the current_revision of an article is
# changed...
