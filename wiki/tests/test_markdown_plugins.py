# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import markdown
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase
from wiki.core.markdown.mdx.codehilite import WikiCodeHiliteExtension
from wiki.core.markdown.mdx.responsivetable import ResponsiveTableExtension
from wiki.models import URLPath
from wiki.plugins.links.mdx.djangowikilinks import WikiPathExtension


try:
    import pygments
    pygments = True  # NOQA
except ImportError:
    pygments = False


class WikiPathExtensionTests(TestCase):
    def test_works_with_lazy_functions(self):
        URLPath.create_root()
        config = (
            ('base_url', reverse_lazy('wiki:get', kwargs={'path': ''})),
        )
        md = markdown.Markdown(
            extensions=['extra', WikiPathExtension(config)]
        )
        text = '[Français](wiki:/fr)'
        self.assertEqual(
            md.convert(text),
            '<p><a class="wikipath linknotfound" href="/fr">Français</a></p>',
        )


class ResponsiveTableExtensionTests(TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[
            'extra',
            ResponsiveTableExtension()
        ])
        self.md_without = markdown.Markdown(extensions=['extra'])

    def test_wrapping(self):
        text = '|th|th|\n|--|--|\n|td|td|'
        expected = '<div class="table-responsive">\n' + self.md_without.convert(text) + '\n</div>'
        self.assertEqual(self.md.convert(text), expected)


class CodehiliteTests(TestCase):

    def test_fenced_code(self):
        md = markdown.Markdown(
            extensions=['extra', WikiCodeHiliteExtension()]
        )
        text = (
            "Code:\n"
            "\n"
            "```python\n"
            "echo 'line 1'\n"
            "echo 'line 2'\n"
            "```\n"
        )
        result = (
            """<p>Code:</p>\n"""
            """<div class="codehilite-wrap"><div class="codehilite"><pre><span></span><span class="n">echo</span> <span class="s1">&#39;line 1&#39;</span>\n"""
            """<span class="n">echo</span> <span class="s1">&#39;line 2&#39;</span>\n"""
            """</pre></div>\n"""
            """</div>"""
        ) if pygments else (
            """<p>Code:</p>\n"""
            """<div class="codehilite-wrap"><pre class="codehilite"><code class="language-python">echo 'line 1'\n"""
            """echo 'line 2'</code></pre>\n"""
            """</div>"""
        )
        self.assertEqual(
            md.convert(text),
            result,
        )

    def test_indented_code(self):
        md = markdown.Markdown(
            extensions=['extra', WikiCodeHiliteExtension()]
        )
        text = (
            "Code:\n"
            "\n"
            "    #!/usr/bin/python\n"
            "    print('line 1')\n"
            "    print('line 2')\n"
            "    print('æøå')\n"
            "\n"
        )
        result = (
            """<p>Code:</p>\n"""
            """<div class="codehilite-wrap"><table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre>1\n"""
            """2\n"""
            """3\n"""
            """4</pre></div></td><td class="code"><div class="codehilite"><pre><span></span><span class="ch">#!/usr/bin/python</span>\n"""
            """<span class="k">print</span><span class="p">(</span><span class="s1">&#39;line 1&#39;</span><span class="p">)</span>\n"""
            """<span class="k">print</span><span class="p">(</span><span class="s1">&#39;line 2&#39;</span><span class="p">)</span>\n"""
            """<span class="k">print</span><span class="p">(</span><span class="s1">&#39;æøå&#39;</span><span class="p">)</span>\n"""
            """</pre></div>\n"""
            """</td></tr></table></div>"""
        ) if pygments else (
            """<p>Code:</p>\n"""
            """<div class="codehilite-wrap"><pre class="codehilite"><code class="language-python linenums">#!/usr/bin/python\n"""
            """print('line 1')\n"""
            """print('line 2')\n"""
            """print('æøå')</code></pre>\n"""
            """</div>"""
        )
        self.assertEqual(
            md.convert(text),
            result,
        )
