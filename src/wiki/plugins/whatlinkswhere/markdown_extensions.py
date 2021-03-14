from urllib.parse import urljoin
from urllib.parse import urlparse

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from wiki.models import URLPath

from . import models


class LinkTreeprocessor(Treeprocessor):
    @property
    def my_urlpath(self):
        try:
            return self._my_urlpath
        except AttributeError:
            pass
        urlpaths = self.md.article.urlpath_set.all()
        if urlpaths.exists():
            self._my_urlpath = urlpaths[0]
        else:
            self._my_urlpath = None
        return self._my_urlpath

    def store_link(self, from_article, el, root):

        href = el.get("href")
        if not href:
            # Anchor, not link
            return

        try:
            url = urlparse(href)
        except ValueError:
            return
        if url.scheme or url.netloc:
            # External link
            return

        # Ensure that path ends with a slash
        target = urljoin(from_article.path, url.path.rstrip("/") + "/")

        try:
            to_article = URLPath.get_by_path(target)
        except URLPath.DoesNotExist:
            # ‘red’ link to unwritten article. (maybe it's worth tracking those in principle)
            return

        # All other cases have been handled: We have an internal link, which
        # should be reflected in the database.
        models.InternalLink.objects.create(
            from_article=from_article.article,
            to_article=to_article.article,
        ).save()

        return

    def run(self, doc):
        from_article = URLPath.get_by_path(self.my_urlpath.path)
        models.InternalLink.objects.filter(from_article=from_article.article).delete()
        wiki_root = URLPath.get_by_path("")

        for el in doc.iter():
            if el.tag != "a":
                continue
            self.store_link(from_article, el, wiki_root)


class LinkExtension(Extension):

    TreeProcessorClass = LinkTreeprocessor

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        ext = self.TreeProcessorClass(md)
        md.treeprocessors.add("whatlinkshere", ext, ">inline")


def makeExtension(*args, **kwargs):
    """Return an instance of the extension."""
    return LinkExtension(*args, **kwargs)
