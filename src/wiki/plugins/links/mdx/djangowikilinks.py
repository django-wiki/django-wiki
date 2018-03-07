"""
Wikipath Extension for Python-Markdown
======================================

Converts [Link Name](wiki:ArticleName) to relative links pointing to article.

Basic usage:

    >>> import markdown
    >>> text = "Some text with a [Link Name](wiki:ArticleName)."
    >>> html = markdown.markdown(text, ['wikipath(base_url="/wiki/view/")'])
    >>> html
    '<p>Some text with a <a class="wikipath" href="/wiki/view/ArticleName/">Link Name</a>.</p>'

Dependencies:
* [Python 3.4+](https://python.org)
* [Markdown 2.6+](https://pypi.python.org/pypi/Markdown)
"""
from os import path as os_path

import markdown
from markdown.util import etree
from wiki import models


class WikiPathExtension(markdown.Extension):

    def __init__(self, configs):
        # set extension defaults
        self.config = {
            'base_url': [
                '/',
                'String to append to beginning of URL.'],
            'html_class': [
                'wikipath',
                'CSS hook. Leave blank for none.'],
            'default_level': [
                2,
                'The level that most articles are created at. Relative links will tend to start at that level.']}

        # Override defaults with user settings
        for key, value in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # append to end of inline patterns
        WIKI_RE = r'\[(?P<label>[^\]]+?)\]\(wiki:(?P<wikipath>[a-zA-Z0-9\./_-]*?)(?P<fragment>#[a-zA-Z0-9\./_-]*)?\)'
        wikiPathPattern = WikiPath(WIKI_RE, self.config, markdown_instance=md)
        wikiPathPattern.md = md
        md.inlinePatterns.add('djangowikipath', wikiPathPattern, "<reference")


class WikiPath(markdown.inlinepatterns.Pattern):

    def __init__(self, pattern, config, **kwargs):
        super().__init__(pattern, **kwargs)
        self.config = config

    def handleMatch(self, m):
        wiki_path = m.group('wikipath')
        absolute = False
        if wiki_path.startswith("/"):
            absolute = True
        wiki_path = wiki_path.strip("/")

        # Use this to calculate some kind of meaningful path
        # from the link, regardless of whether or not something can be
        # looked up
        path_from_link = ""

        if absolute:
            base_path = self.config['base_url'][0]
            path_from_link = os_path.join(str(base_path), wiki_path)

            urlpath = None
            path = path_from_link
            try:
                urlpath = models.URLPath.get_by_path(wiki_path)
                path = urlpath.get_absolute_url()
            except models.URLPath.DoesNotExist:
                pass
        else:
            urlpath = models.URLPath.objects.get(article=self.markdown.article)
            source_components = urlpath.path.strip("/").split("/")
            # We take the first (self.config['default_level'] - 1) components, so adding
            # one more component would make a path of length
            # self.config['default_level']
            starting_level = max(0, self.config['default_level'][0] - 1)
            starting_path = "/".join(source_components[: starting_level])

            path_from_link = os_path.join(starting_path, wiki_path)

            lookup = models.URLPath.objects.none()
            if urlpath.parent:
                lookup = urlpath.parent.get_descendants().filter(
                    slug=wiki_path)
            else:
                lookup = urlpath.get_descendants().filter(slug=wiki_path)

            if lookup.count() > 0:
                urlpath = lookup[0]
                path = urlpath.get_absolute_url()
            else:
                urlpath = None
                path = self.config['base_url'][0] + path_from_link

        label = m.group('label')
        fragment = m.group('fragment') or ""

        a = etree.Element('a')
        a.set('href', path + fragment)
        if not urlpath:
            a.set('class', self.config['html_class'][0] + " linknotfound")
        else:
            a.set('class', self.config['html_class'][0])
        a.text = label

        return a

    def _getMeta(self):
        """ Return meta data or config data. """
        base_url = self.config['base_url'][0]
        html_class = self.config['html_class'][0]
        if hasattr(self.md, 'Meta'):
            if 'wiki_base_url' in self.md.Meta:
                base_url = self.md.Meta['wiki_base_url'][0]
            if 'wiki_html_class' in self.md.Meta:
                html_class = self.md.Meta['wiki_html_class'][0]
        return base_url, html_class


def makeExtension(configs=None):
    return WikiPathExtension(configs=configs)
