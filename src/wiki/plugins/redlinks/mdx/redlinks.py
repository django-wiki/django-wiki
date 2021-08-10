import html
from urllib.parse import urljoin
from urllib.parse import urlparse

import wiki
from django.urls import resolve
from django.urls.exceptions import Resolver404
from markdown.extensions import Extension
from markdown.postprocessors import AndSubstitutePostprocessor
from markdown.treeprocessors import Treeprocessor
from wiki.core.markdown import add_to_registry
from wiki.decorators import which_article
from wiki.models import Article
from wiki.models import URLPath


class LinkTreeprocessor(Treeprocessor):
    def __init__(self, md, config):
        super().__init__(md)
        self.md = md
        self.broken_class = config["broken"]
        self.internal_class = config["internal"]
        self.external_class = config["external"]

    @property
    def my_urlpath(self):
        try:
            return self._my_urlpath
        except AttributeError:
            self._my_urlpath = self.md.article.get_absolute_url()
            return self._my_urlpath

    def get_class(self, el):  # noqa: max-complexity 11
        href = el.get("href")
        if not href:
            return
        # The autolinker turns email links into links with many HTML entities.
        # These entities are further escaped using markdown-specific codes.
        # First unescape the markdown-specific, then use html.unescape.
        href = AndSubstitutePostprocessor().run(href)
        href = html.unescape(href)
        try:
            url = urlparse(href)
        except ValueError:
            return
        if url.scheme == "mailto":
            return
        if url.scheme or url.netloc:
            # Contains a hostname or url schema ⇒ External link
            return self.external_class
        # Ensure that path ends with a slash
        relpath = url.path.rstrip("/") + "/"
        try:
            target = resolve(urljoin(self.my_urlpath, relpath))
        except Resolver404:
            # Broken absolute link
            return self.external_class

        if target.app_names != ["wiki"]:
            # Links outside wiki
            return self.external_class

        try:
            article, urlpath = which_article(**target.kwargs)
        except (
            wiki.core.exceptions.NoRootURL,
            URLPath.DoesNotExist,
            Article.DoesNotExist,
        ):
            return self.broken_class

        return self.internal_class

    def run(self, doc):
        for el in doc.iter():
            if el.tag != "a":
                continue
            class_ = self.get_class(el)
            if class_:
                # Append class
                classes = (el.get("class", "") + " " + class_).strip()
                el.set("class", classes)


class LinkExtension(Extension):

    TreeProcessorClass = LinkTreeprocessor

    def __init__(self, *args, **kwargs):
        self.config = {
            "broken": ["wiki-broken", "CSS class to use for broken internal links"],
            "internal": ["wiki-internal", "CSS class to use for internal links"],
            "external": ["wiki-external", "CSS class to use for external links"],
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        ext = self.TreeProcessorClass(md, self.getConfigs())

        add_to_registry(md.treeprocessors, "redlinks", ext, ">inline")


def makeExtension(*args, **kwargs):
    """Return an instance of the extension."""
    return LinkExtension(*args, **kwargs)
