Mediawiki
=========

If you want to import from Mediawiki you can create an XML dump of the pages and then use
a management command for your app to import it.

The following management command code should work fine with the latest django-wiki version and
latest mediawiki version.
It uses the lxml library to parse the mediawiki xml
and the unidecode to convert non-latin characters to ascii (so as to create their slug). Finally it
uses pandoc to do the actual markdown -> github flavored markdown convert (I have tested it on windows and it works great).

For the lxml and unidecode you can install them with ``pip install lxml unidecode`` and for pandoc you can
download it from https://pandoc.org/installing.html (make sure the pandoc binary is in your PATH).

Finally, you can add the following management command to a ``management/commands/import_mediawiki_dump``
module and run it with
``python manage.py import_mediawiki_dump <mediawiki-xml-dump-file>``


..  code-block:: python

    from django.core.management.base import BaseCommand
    from wiki.models.article import ArticleRevision, Article
    from wiki.models.urlpath import URLPath
    from django.contrib.sites.models import Site
    from django.template.defaultfilters import slugify
    import unidecode
    from django.contrib.auth import get_user_model
    import datetime
    import pytz
    from django.db import transaction
    import subprocess
    from lxml import etree


    def slugify2(s):
        return slugify(unidecode.unidecode(s))


    def convert_to_markdown(text):
        proc = subprocess.Popen(
            ["pandoc", "-f", "mediawiki", "-t", "gfm"],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        proc.stdin.write(text.encode("utf-8"))
        proc.stdin.close()
        return proc.stdout.read().decode("utf-8")


    def create_article(title, text, timestamp, user):
        text_ok = (
            text.replace("__NOEDITSECTION__", "")
            .replace("__NOTOC__", "")
            .replace("__TOC__", "")
        )

        text_ok = convert_to_markdown(text_ok)

        article = Article()
        article_revision = ArticleRevision()
        article_revision.content = text_ok
        article_revision.title = title
        article_revision.user = user
        article_revision.owner = user
        article_revision.created = timestamp
        article.add_revision(article_revision, save=True)
        article_revision.save()
        article.save()
        return article


    def create_article_url(article, slug, current_site, url_root):
        upath = URLPath.objects.create(
            site=current_site, parent=url_root, slug=slug, article=article
        )
        article.add_object_relation(upath)


    def import_page(current_site, url_root, text, title, timestamp, replace_existing, user):
        slug = slugify2(title)

        try:
            urlp = URLPath.objects.get(slug=slug)

            if not replace_existing:
                print("\tAlready existing, skipping...")
                return

            print("\tDestorying old version of the article")
            urlp.article.delete()

        except URLPath.DoesNotExist:
            pass

        article = create_article(title, text, timestamp, user)
        create_article_url(article, slug, current_site, url_root)


    class Command(BaseCommand):
        help = "Import everything from a MediaWiki XML dump file. Only the latest version of each page is imported."
        args = ""

        def add_arguments(self, parser):
            parser.add_argument("file", type=str)

        @transaction.atomic()
        def handle(self, *args, **options):
            user = get_user_model().objects.get(username="root")
            current_site = Site.objects.get_current()
            url_root = URLPath.root()

            tree = etree.parse(options["file"])
            pages = tree.xpath('// *[local-name()="page"]')
            for p in pages:
                title = p.xpath('*[local-name()="title"]')[0].text
                print(title)
                revision = p.xpath('*[local-name()="revision"]')[0]
                text = revision.xpath('*[local-name()="text"]')[-1].text
                timestamp = revision.xpath('*[local-name()="timestamp"]')[0].text
                timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
                timestamp_with_timezone = pytz.utc.localize(timestamp)

                import_page(
                    current_site,
                    url_root,
                    text,
                    title,
                    timestamp_with_timezone,
                    True,
                    user,
            )

Please notice that this tries to find a ``root`` user to assign the owner of the imported pages
(you can leave that as None or add your own user).
Also I haven't tested if it works fine when you've got multiple revisions of each page;
it tries to pick the text of the latest one (``text = revision.xpath('*[local-name()="text"]')[-1].text``)
but I'm not sure it will work properly. Better to be safe by including only the latest revision of each
article on your mediawiki dump. Of course you can modify the code to add all the revisions of each page
if you want instead of only the latest one.

Also you can pass True or False to import_page in order to replace or skip existing pages.
