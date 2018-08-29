from tests.base import RequireRootArticleMixin, TestBase
from wiki.core import markdown


class MacroTests(RequireRootArticleMixin, TestBase):
    def test_article_list(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("[article_list depth:2]")
        self.assertIn("Nothing below this level", md_text)
        self.assertNotIn("[article_list depth:2]", md_text)

    def test_escape(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("`[article_list depth:2]`")
        self.assertNotIn("Nothing below this level", md_text)
        self.assertIn("[article_list depth:2]", md_text)
