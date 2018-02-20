import markdown
from django.test import TestCase
from django.urls import reverse_lazy
from wiki.models import URLPath
from wiki.plugins.links.mdx.djangowikilinks import WikiPathExtension


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

        URLPath.create_urlpath(URLPath.root(), "linktest",
                               title="LinkTest",
                               content="A page\n#A section\nA line",
                               user_message="Comment1")

        # Link to an existing page
        text = '[Test link](wiki:/linktest)'
        self.assertEqual(
            md.convert(text),
            '<p><a class="wikipath" href="/linktest/">Test link</a></p>',
        )

        # Link with an empty fragment
        text = '[Test link](wiki:/linktest#)'
        self.assertEqual(
            md.convert(text),
            '<p><a class="wikipath" href="/linktest/#">Test link</a></p>',
        )

        # Link to a header in an existing page
        text = '[Test head](wiki:/linktest#wiki-toc-a-section)'
        self.assertEqual(
            md.convert(text),
            '<p><a class="wikipath" href="/linktest/#wiki-toc-a-section">Test head</a></p>',
        )

        # Link to a header in a non existing page
        text = '[Test head nonExist](wiki:/linktesterr#wiki-toc-a-section)'
        self.assertEqual(
            md.convert(text),
            '<p><a class="wikipath linknotfound" href="/linktesterr#wiki-toc-a-section">Test head nonExist</a></p>',
        )

        # Invalid Wiki link: The default markdown link parser takes over
        text = '[Test head err](wiki:/linktest#wiki-toc-a-section#err)'
        self.assertEqual(
            md.convert(text),
            '<p><a href="wiki:/linktest#wiki-toc-a-section#err">Test head err</a></p>',
        )
