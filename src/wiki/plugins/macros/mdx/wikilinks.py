#!/usr/bin/env python
"""
Extend the shipped Markdown extension 'wikilinks'
"""
from __future__ import unicode_literals

import re

import markdown
from django.core.urlresolvers import reverse
from markdown.extensions import wikilinks


def build_url(label, base, end, md):
    """ Build a url from the label, a base, and an end. """
    clean_label = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', label)
    urlpaths = md.article.urlpath_set.all()
    # Nevermind about the base we are fed, just keep the original
    # call pattern from the wikilinks plugin for later...
    base = reverse('wiki:get', kwargs={'path': ''})
    for urlpath in urlpaths:
        if urlpath.children.filter(slug=clean_label).exists():
            base = ''
            break
    return '%s%s%s' % (base, clean_label, end)


class WikiLinkExtension(wikilinks.WikiLinkExtension):

    def __init__(self, configs={}):
        # set extension defaults
        self.config = {
            'base_url': ['', 'String to append to beginning or URL.'],
            'end_url': ['/', 'String to append to end of URL.'],
            'html_class': ['wiki_wikilink', 'CSS hook. Leave blank for none.'],
            'build_url': [build_url, 'Callable formats URL from label.'],
        }

        # Override defaults with user settings
        for key, value in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # append to end of inline patterns
        WIKILINK_RE = r'\[\[([\w0-9_ -]+)\]\]'
        wikilinkPattern = WikiLinks(WIKILINK_RE, self.getConfigs())
        wikilinkPattern.md = md
        md.inlinePatterns.add('wikilink', wikilinkPattern, "<not_strong")


class WikiLinks(wikilinks.WikiLinks):

    def handleMatch(self, m):
        if m.group(2).strip():
            base_url, end_url, html_class = self._getMeta()
            label = m.group(2).strip()
            url = self.config['build_url'](label, base_url, end_url, self.md)
            a = markdown.util.etree.Element('a')
            a.text = label
            a.set('href', url)
            if html_class:
                a.set('class', html_class)
        else:
            a = ''
        return a
