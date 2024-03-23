Mediawiki
=========

If you want to import articles from Mediawiki, you can create an XML dump of the pages and then use
a Django management command to import it.
The management command is not provided as part of django-wiki, but we'll show you how to build one for your own Django app.

In the management command, we are going to use the lxml library to parse the MediaWiki XML
and the unidecode to convert non-latin characters to ascii (so as to create their slug). Finally it
uses pandoc to do conversion from MediaWiki markup to GitHub Flavored Markdown (which in this case renders fine in django-wiki).

For the lxml and unidecode you can install them with ``pip install lxml unidecode`` and for pandoc you can
download it from https://pandoc.org/installing.html (make sure the pandoc binary is in your PATH).

The following snippet of code should be placed in ``<your-app>/management/commands/import_mediawiki_dump.py``:


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

Usage
-----

Once the management command is provided by your Django application, you can invoke it from the command-line:

.. code-block:: console

   python manage.py import_mediawiki_dump <mediawiki-xml-dump-file>``

Further work and customizing
----------------------------

Please note the following:

- The script defines a ``root`` user to assign the owner of the imported pages (you can leave that as None or add your own user).

- Multiple revisions of each page have not been implemented. Instead, the script tries to pick the text of the latest one (``text = revision.xpath('*[local-name()="text"]')[-1].text``). Because of this, it's recommended to only include the latest revision of each article on your MediaWiki dump.

- You can pass ``True`` or ``False`` to ``import_page()`` in order to replace or skip existing pages.
