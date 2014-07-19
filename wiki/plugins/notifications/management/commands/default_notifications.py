from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from wiki.plugins.notifications.settings import ARTICLE_EDIT

from wiki.plugins.notifications.models import ArticleSubscription
from wiki.models import ArticleRevision, Article

from django_nyt.utils import subscribe
from django_nyt.models import Settings

class Command(BaseCommand):
    # @ReservedAssignment
    help = 'Creates notifications for all article revision authors'

    def handle(self, *args, **options):
        
        user_settings = {}
        
        content_type = ContentType.objects.get_for_model(Article)
        
        for revision in ArticleRevision.objects.filter(deleted=False).exclude(user=None):
            
            if not revision.user in user_settings:
                user_settings[revision.user], __ = Settings.objects.get_or_create(user=revision.user)
            
            subscription = subscribe(
                user_settings[revision.user],
                ARTICLE_EDIT,
                content_type=content_type,
            )
            
            ArticleSubscription.objects.get_or_create(
                subscription=subscription,
                article=revision.article
            )
