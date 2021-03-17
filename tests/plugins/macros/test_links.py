from wiki.core import markdown

from tests.base import RequireRootArticleMixin
from tests.base import TestBase


class WikiLinksTests(RequireRootArticleMixin, TestBase):
    def test_wikilink(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("[[Root Article]]")
        self.assertEqual(
            md_text,
            '<p><a class="wiki_wikilink wiki-broken" href="/Root_Article/">Root Article</a></p>',
        )
