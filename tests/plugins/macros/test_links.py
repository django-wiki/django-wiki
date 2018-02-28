from tests.base import RequireRootArticleMixin, TestBase
from wiki.core import markdown
from wiki.plugins.macros.mdx.wikilinks import WikiLinkExtension


class WikiLinksTests(RequireRootArticleMixin, TestBase):
    def test_wikilink(self):
        md = markdown.ArticleMarkdown(article=self.root_article, extensions=[WikiLinkExtension()])
        md_text = md.convert('[[Root Article]]')
        self.assertEqual(
            md_text, '<p><a class="wiki_wikilink" href="/Root_Article/">Root Article</a></p>'
        )
