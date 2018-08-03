from tests.base import RequireRootArticleMixin, TestBase
from wiki.core import markdown


class ImageMarkdownTests(RequireRootArticleMixin, TestBase):
    def test_markdown(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("[image:1 align:left]")
        self.assertIn("<figure", md_text)
        self.assertNotIn("[image:1 align:left]", md_text)

    def test_escape(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("`[image:1 align:left]`")
        self.assertNotIn("<figure", md_text)
        self.assertIn("[image:1 align:left]", md_text)
