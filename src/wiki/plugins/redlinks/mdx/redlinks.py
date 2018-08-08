import html
from urllib.parse import urljoin, urlparse

from markdown.extensions import Extension
from markdown.postprocessors import AndSubstitutePostprocessor
from markdown.treeprocessors import Treeprocessor
from wiki.models import URLPath


def urljoin_internal(base, url):
    """
    Combine a base URL with a relative URL while ensuring that the relative
    URL does not go outside the hierarchy containing the base URL.

    >>> print(urljoin_internal("foo/bar/", "../baz/"))
    foo/baz/
    >>> print(urljoin_internal("foo/bar/", "../../baz/"))
    baz/
    >>> print(urljoin_internal("foo/bar/", "../../../baz/"))
    None
    """

    canary1 = "//a/a/"
    canary2 = "//a/b/"
    res1 = urljoin(canary1 + base, url)
    res2 = urljoin(canary2 + base, url)
    if res1.startswith(canary1) and res2.startswith(canary2):
        return res1[len(canary1):]


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
            pass
        urlpaths = self.md.article.urlpath_set.all()
        if urlpaths.exists():
            self._my_urlpath = urlpaths[0]
        else:
            self._my_urlpath = None
        return self._my_urlpath

    def get_class(self, el):
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
        if url.scheme or url.netloc or url.path.startswith("/"):
            # Contains a hostname or is an absolute link => external
            return self.external_class
        # Ensure that path ends with a slash
        relpath = url.path.rstrip("/") + "/"
        target = urljoin_internal(self.my_urlpath.path, relpath)
        if target is None:
            # Relative path goes outside wiki URL space => external
            return self.external_class
        try:
            URLPath.get_by_path(target)
        except URLPath.DoesNotExist:
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

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        self.md = md
        ext = self.TreeProcessorClass(md, self.getConfigs())
        md.treeprocessors.add("redlinks", ext, ">inline")


def makeExtension(*args, **kwargs):
    """Return an instance of the extension."""
    return LinkExtension(*args, **kwargs)
