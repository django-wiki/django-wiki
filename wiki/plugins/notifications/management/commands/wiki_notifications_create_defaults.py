# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils import translation


class Command(BaseCommand):
    args = '[file-name.csv]'
    help = 'Import and parse messages directly from a CSV file.'  # @ReservedAssignment

    def handle(self, *args, **options):
        from django.conf import settings
        translation.activate(settings.LANGUAGE_CODE)
        
        from django.contrib.auth import get_user_model
        from wiki.plugins.notifications import models
        from wiki.plugins.notifications.settings import ARTICLE_EDIT
        from wiki.models import Article
        from django_nyt.utils import subscribe
        from django_nyt.models import Settings
        from django.contrib.contenttypes.models import ContentType
        
        # User: Settings
        settings_map = {}
        
        def subscribe_to_article(article, user):
            if user not in settings_map:
                settings_map[user], __ = Settings.objects.get_or_create(user=user)
            
            return subscribe(settings_map[user], ARTICLE_EDIT, content_type=ContentType.objects.get_for_model(article), object_id=article.id)
            
        for article in Article.objects.all():
            if article.owner:
                subscription = subscribe_to_article(article, article.owner)
                models.ArticleSubscription.objects.get_or_create(article=article, subscription=subscription)
            for revision in article.articlerevision_set.exclude(user=article.owner).exclude(user=None).values('user').distinct():
                user = get_user_model().objects.get(id=revision['user'])
                subscription = subscribe_to_article(article, user)
                models.ArticleSubscription.objects.get_or_create(article=article, subscription=subscription)
        
        translation.deactivate()