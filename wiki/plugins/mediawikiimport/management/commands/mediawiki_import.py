from __future__ import absolute_import, print_function, unicode_literals

import getpass
import string
import urllib
from optparse import make_option

import six
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify, striptags
from wiki.models.article import Article, ArticleRevision
from wiki.models.urlpath import URLPath


def only_printable(s):
    return ''.join([x for x in s if x in string.printable])


class Command(BaseCommand):
    help = 'Import everything from a MediaWiki'
    args = 'ApiUrl Username [Password]'

    articles_worked_on = []
    articles_imported = []
    matching_old_link_new_link = {}

    option_list = BaseCommand.option_list + (
        make_option(
            '--user-matching',
            action='append',
            dest='user_matching',
            default=[],
            help='List of <username>:django_user_pk to do the matchin'),
        make_option(
            '--replace_existing',
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
            raise CommandError(
                'You need to provide the url to the MediaWiki API')

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

        result = api.APIRequest(
            site, {
                'action': 'query', 'generator': 'allpages'}).query()

        return listFromQuery(site, result['query']['pages'])

    def import_page(
            self,
            api,
            site,
            page,
            current_site,
            url_root,
            user_matching,
            replace_existing):

        import pypandoc

        # Filter titles, to avoid stranges charaters.
        title = only_printable(page.title)
        urltitle = slugify(only_printable(urllib.unquote(page.urltitle))[:50])

        added = 1

        while urltitle in self.articles_worked_on:
            title = only_printable("{} {}".format(page.title, added))
            urltitle = slugify(
                "{} {}".format(only_printable(urllib.unquote(page.urltitle))[:47], added)
            )

            added += 1

        self.articles_worked_on.append(urltitle)

        print("Working on {} ({})".format(title, urltitle))

        # Check if the URL path already exists
        try:
            urlp = URLPath.objects.get(slug=urltitle)

            self.matching_old_link_new_link[
                page.title] = urlp.article.get_absolute_url()

            if not replace_existing:
                print("\tAlready existing, skipping...")
                return

            print("\tDestorying old version of the article")
            urlp.article.delete()

        except URLPath.DoesNotExist:
            pass

        # Create article
        article = Article()

        for history_page in page.getHistory()[::-1]:

            try:
                if history_page['user'] in user_matching:
                    user = get_user_model().objects.get(
                        pk=user_matching[
                            history_page['user']])
                else:
                    user = get_user_model().objects.get(
                        username=history_page['user'])
            except get_user_model().DoesNotExist:
                print(
                    "\tCannot found user with username={}. Use --user-matching \"{}:<user_pk>\" to manualy set it".format(
                        history_page['user'], history_page['user'])
                )
                user = None

            article_revision = ArticleRevision()
            article_revision.content = pypandoc.convert(
                history_page['*'],
                'md',
                'mediawiki')
            article_revision.title = title
            article_revision.user = user
            article_revision.owner = user

            article.add_revision(article_revision, save=True)

            article_revision.created = history_page['timestamp']
            article_revision.save()

        # Updated lastest content WITH expended templates
        # TODO ? Do that for history as well ?
        article_revision.content = pypandoc.convert(
            striptags(
                page.getWikiText(
                    True,
                    True).decode('utf-8')).replace(
                '__NOEDITSECTION__',
                '').replace(
                    '__NOTOC__',
                    ''),
            'md',
            'mediawiki')
        article_revision.save()

        article.save()

        upath = URLPath.objects.create(
            site=current_site,
            parent=url_root,
            slug=urltitle,
            article=article)
        article.add_object_relation(upath)

        self.matching_old_link_new_link[
            page.title] = upath.article.get_absolute_url()

        self.articles_imported.append((article, article_revision))

    def update_links(self):
        """Update link in imported articles"""

        # TODO: nsquare is bad
        for (article, article_revision) in self.articles_imported:
            print("Updating links of {}".format(article_revision.title))
            for id_from, id_to in six.iteritems(
                    self.matching_old_link_new_link):
                print(
                    "Replacing ({} \"wikilink\") with ({})".format(id_from, id_to)
                )
                article_revision.content = article_revision.content.replace(
                    "({} \"wikilink\")".format(id_from),
                    "({})".format(id_to)
                )

            article_revision.save()

    def handle(self, *args, **options):

        try:
            import wikitools
        except ImportError:
            raise CommandError(
                'You need to install wikitools to use this command !')

        try:
            import pypandoc  # noqa @UnusedImport
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
            self.import_page(
                wikitools.api,
                site,
                page,
                current_site,
                url_root,
                user_matching,
                options['replace_existing'])

        self.update_links()
