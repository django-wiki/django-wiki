from django.core.management.base import BaseCommand, CommandError
import getpass


from wiki.models.article import ArticleRevision, ArticleForObject, Article
from wiki.models.urlpath import URLPath
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from optparse import make_option


class Command(BaseCommand):
    help = 'Import everything from a MediaWiki'
    args = 'ApiUrl Username [Password]'

    option_list = BaseCommand.option_list + (
        make_option('--user-matching',
            action='append',
            dest='user_matching',
            default=[],
            help='List of <username>:django_user_pk to do the matchin'),
        make_option('--replace_existing',
            action='store_true',
            dest='replace_existing',
            default=False,
            help='Replace existing pages'),
    )

    def get_params(self, args):
        """Return the list of params"""
        try:
            api_url = args[0]
        except IndexError:
            raise CommandError('You need to provide the url to the MediaWiki API')

        try:
            api_username = args[1]
        except IndexError:
            raise CommandError('You need to provide an username')

        try:
            api_password = args[2]
        except IndexError:
            api_password = getpass.getpass('Please enter the API password: ')

            if not api_password:
                raise CommandError('You need to provide a password')

        return (api_url, api_username, api_password)

    def get_all_pages(self, api, site):
        """Return all pages on the wiki"""

        from wikitools.pagelist import listFromQuery

        result = api.APIRequest(site, {'action': 'query', 'generator': 'allpages'}).query()

        return listFromQuery(site, result['query']['pages'])

    def import_page(self, api, site, page, current_site, url_root, user_matching, replace_existing):

        import pypandoc

        print "Working on %s (%s)" % (page.title, page.urltitle)

        # Check if the URL path already exists
        try:
            urlp = URLPath.objects.get(slug=page.urltitle[:50])

            if not replace_existing:
                print "\tAlready existing, skipping..."
                return

            print "\tDestorying old version of the article"
            urlp.article.delete()

        except URLPath.DoesNotExist:
            pass

        # Create article
        article = Article()

        for history_page in page.getHistory()[::-1]:

            try:
                if history_page['user'] in user_matching:
                    user = get_user_model().objects.get(pk=user_matching[history_page['user']])
                else:
                    user = get_user_model().objects.get(username=history_page['user'])
            except get_user_model().DoesNotExist:
                print "\tCannot found user with username=%s. Use --user-matching \"%s:<user_pk>\" to manualy set it" % (history_page['user'], history_page['user'], )
                user = None

            article_revision = ArticleRevision()
            article_revision.content = pypandoc.convert(history_page['*'], 'md', 'mediawiki')
            article_revision.title = page.title
            article_revision.user = user
            article_revision.owner = user

            article.add_revision(article_revision, save=True)

            article_revision.created = history_page['timestamp']
            article_revision.save()

        article.save()

        upath = URLPath.objects.create(site=current_site, parent=url_root, slug=page.urltitle[:50], article=article)
        article.add_object_relation(upath)

    def handle(self, *args, **options):

        try:
            import wikitools
        except ImportError:
            raise CommandError('You need to install wikitools to use this command !')

        try:
            import pypandoc
        except ImportError:
            raise CommandError('You need to install pypandoc')

        user_matching = {}

        for um in options['user_matching']:
            mu = um[::-1]
            kp, emanresu = mu.split(':', 1)

            pk = kp[::-1]
            username = emanresu[::-1]

            user_matching[username] = pk

        api_url, api_username, api_password = self.get_params(args)

        site = wikitools.wiki.Wiki(api_url)
        site.login(api_username, api_password)

        pages = self.get_all_pages(wikitools.api, site)

        current_site = Site.objects.get_current()
        url_root = URLPath.root()

        for page in pages:
            self.import_page(wikitools.api, site, page, current_site, url_root, user_matching, options['replace_existing'])
