from tests.base import RequireRootArticleMixin, TestBase
from wiki.core import markdown


class WikiLinksTests(RequireRootArticleMixin, TestBase):
    def test_wikilink(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert('[[Root Article]]')
        self.assertEqual(
            md_text, '<p><a class="wiki_wikilink wiki-external" href="/Root_Article/">Root Article</a></p>'
        )
