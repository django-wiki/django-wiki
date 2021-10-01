import markdown
from ddt import data
from ddt import ddt
from ddt import unpack
from django.test import TestCase
from django.urls import reverse_lazy
from wiki.models import URLPath
from wiki.plugins.links.mdx.djangowikilinks import WikiPathExtension

from tests.base import wiki_override_settings

FIXTURE_POSITIVE_MATCHES_TRAILING_SLASH = [
    (
        "[Français](wiki:/fr)",
        '<p><a class="wikipath linknotfound" href="/fr/">Français</a></p>',
    ),
    (
        # Link to an existing page
        "[Test link](wiki:/linktest)",
        '<p><a class="wikipath" href="/linktest/">Test link</a></p>',
    ),
    (
        # Link with an empty fragment
        "[Test link](wiki:/linktest#)",
        '<p><a class="wikipath" href="/linktest/#/">Test link</a></p>',
    ),
    (
        # Link to a header in an existing page
        "[Test head](wiki:/linktest#wiki-toc-a-section)",
        '<p><a class="wikipath" href="/linktest/#wiki-toc-a-section/">Test head</a></p>',
    ),
    (
        # Link to a header in a non existing page
        "[Test head nonExist](wiki:/linktesterr#wiki-toc-a-section)",
        '<p><a class="wikipath linknotfound" href="/linktesterr#wiki-toc-a-section/">Test head nonExist</a></p>',
    ),
    (
        # Invalid Wiki link: The default markdown link parser takes over
        "[Test head err](wiki:/linktest#wiki-toc-a-section#err)",
        '<p><a href="wiki:/linktest#wiki-toc-a-section#err">Test head err</a></p>',
    ),
]
FIXTURE_POSITIVE_MATCHES_NO_TRAILING_SLASH = [
    (
        "[Français](wiki:/fr)",
        '<p><a class="wikipath linknotfound" href="/fr">Français</a></p>',
    ),
    (
        # Link to an existing page
        "[Test link](wiki:/linktest)",
        '<p><a class="wikipath" href="/linktest">Test link</a></p>',
    ),
    (
        # Link with an empty fragment
        "[Test link](wiki:/linktest#)",
        '<p><a class="wikipath" href="/linktest/#">Test link</a></p>',
    ),
    (
        # Link to a header in an existing page
        "[Test head](wiki:/linktest#wiki-toc-a-section)",
        '<p><a class="wikipath" href="/linktest/#wiki-toc-a-section">Test head</a></p>',
    ),
    (
        # Link to a header in a non existing page
        "[Test head nonExist](wiki:/linktesterr#wiki-toc-a-section)",
        '<p><a class="wikipath linknotfound" href="/linktesterr#wiki-toc-a-section">Test head nonExist</a></p>',
    ),
    (
        # Invalid Wiki link: The default markdown link parser takes over
        "[Test head err](wiki:/linktest#wiki-toc-a-section#err)",
        '<p><a href="wiki:/linktest#wiki-toc-a-section#err">Test head err</a></p>',
    ),
]


@ddt
class WikiPathExtensionTests(TestCase):
    """
    Test the wikilinks markdown plugin.
    I could not get it to work with `@pytest.mark.parametrize` so using `ddt` instead
    """

    def setUp(self):
        config = (("base_url", reverse_lazy("wiki:get", kwargs={"path": ""})),)
        self.md = markdown.Markdown(extensions=["extra", WikiPathExtension(config)])
        URLPath.create_root()
        URLPath.create_urlpath(
            URLPath.root(),
            "linktest",
            title="LinkTest",
            content="A page\n#A section\nA line",
            user_message="Comment1",
        )

    @wiki_override_settings(WIKI_WIKILINKS_TRAILING_SLASH=True)
    @data(*FIXTURE_POSITIVE_MATCHES_TRAILING_SLASH)
    @unpack
    def test_works_with_lazy_functions_slashes(self, markdown_input, expected_output):
        self.assertEqual(
            self.md.convert(markdown_input),
            expected_output,
        )

    @wiki_override_settings(WIKI_WIKILINKS_TRAILING_SLASH=False)
    @data(*FIXTURE_POSITIVE_MATCHES_NO_TRAILING_SLASH)
    @unpack
    def test_works_with_lazy_functions_no_slashes(
        self, markdown_input, expected_output
    ):
        self.assertEqual(
            self.md.convert(markdown_input),
            expected_output,
        )
