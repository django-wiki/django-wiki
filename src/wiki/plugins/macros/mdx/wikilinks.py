"""
Extend the shipped Markdown extension 'wikilinks'
"""
import re

import markdown
from django.urls import reverse
from markdown.extensions import Extension, wikilinks


def build_url(label, base, end, md):
    """ Build a url from the label, a base, and an end. """
    clean_label = re.sub(r"([ ]+_)|(_[ ]+)|([ ]+)", "_", label)
    urlpaths = md.article.urlpath_set.all()
    # Nevermind about the base we are fed, just keep the original
    # call pattern from the wikilinks plugin for later...
    base = reverse("wiki:get", kwargs={"path": ""})
    for urlpath in urlpaths:
        if urlpath.children.filter(slug=clean_label).exists():
            base = ""
            break
    return "%s%s%s" % (base, clean_label, end)


class WikiLinkExtension(Extension):
    def __init__(self, **kwargs):
        # set extension defaults
        self.config = {
            "base_url": ["", "String to append to beginning or URL."],
            "end_url": ["/", "String to append to end of URL."],
            "html_class": ["wiki_wikilink", "CSS hook. Leave blank for none."],
            "build_url": [build_url, "Callable formats URL from label."],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        self.md = md

        # append to end of inline patterns
        WIKILINK_RE = r"\[\[([\w0-9_ -]+)\]\]"
        wikilinkPattern = WikiLinks(WIKILINK_RE, self.getConfigs())
        wikilinkPattern.md = md
        md.inlinePatterns.add("wikilink", wikilinkPattern, "<not_strong")


class WikiLinks(wikilinks.WikiLinksInlineProcessor):
    def handleMatch(self, m, data):
        base_url, end_url, html_class = self._getMeta()
        label = m.group(1).strip()
        url = self.config["build_url"](label, base_url, end_url, self.md)
        a = markdown.util.etree.Element("a")
        a.text = label
        a.set("href", url)
        if html_class:
            a.set("class", html_class)
        return a, m.start(0), m.end(0)


def makeExtension(*args, **kwargs):
    """Return an instance of the extension."""
    return WikiLinkExtension(*args, **kwargs)
