from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils import translation
from django_nyt.models import Settings
from django_nyt.utils import subscribe
from wiki.models import Article
from wiki.plugins.notifications import models
from wiki.plugins.notifications.settings import ARTICLE_EDIT


class Command(BaseCommand):
    args = '[file-name.csv]'
    # @ReservedAssignment
    help = 'Import and parse messages directly from a CSV file.'

    def handle(self, *args, **options):
        from django.conf import settings

        with translation.override(language=settings.LANGUAGE_CODE):

            # User: Settings
            settings_map = {}

            def subscribe_to_article(article, user):
                if user not in settings_map:
                    settings_map[user], __ = Settings.objects.get_or_create(
                        user=user)

                return subscribe(
                    settings_map[user],
                    ARTICLE_EDIT,
                    content_type=ContentType.objects.get_for_model(article),
                    object_id=article.id)

            subs = 0
            articles = Article.objects.all()
            for article in articles:
                if article.owner:
                    subscription = subscribe_to_article(article, article.owner)
                    models.ArticleSubscription.objects.get_or_create(
                        article=article,
                        subscription=subscription)
                    subs += 1
                for revision in article.articlerevision_set.exclude(
                        user=article.owner).exclude(
                        user=None).values('user').distinct():
                    user = get_user_model().objects.get(id=revision['user'])
                    subs += 1
                    subscription = subscribe_to_article(article, user)
                    models.ArticleSubscription.objects.get_or_create(
                        article=article,
                        subscription=subscription)

            self.stdout.write("Created {subs:d} subscriptions on  {arts:d} articles".format(
                subs=subs,
                arts=articles.count(),
            ), ending='\n')
