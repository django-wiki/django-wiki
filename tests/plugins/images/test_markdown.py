from tests.base import RequireRootArticleMixin, TestBase
from wiki.core import markdown


class ImageMarkdownTests(RequireRootArticleMixin, TestBase):
    def test_before_and_after(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("before [image:1 align:left] after")
        before_pos = md_text.index('before')
        figure_pos = md_text.index('<figure')
        after_pos = md_text.index('after')
        self.assertTrue(before_pos < figure_pos < after_pos)

    def test_markdown(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("[image:1 align:left]")
        self.assertIn("<figure", md_text)
        self.assertNotIn("[image:1 align:left]", md_text)
        md_text = md.convert("image: [image:1 align:left]\nadasd")
        self.assertIn("<figure", md_text)
        md_text = md.convert("image: [image:1 align:right medium]\nadasd")
        self.assertIn("<img src", md_text)
        md_text = md.convert("image: [image:123 align:left medium]\nadasd")
        self.assertIn("Image not found", md_text)

    def test_escape(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("`[image:1 align:left]`")
        self.assertNotIn("<figure", md_text)
        self.assertIn("[image:1 align:left]", md_text)
        md_text = md.convert("`image tag: [image:1]`")
        self.assertIn("image tag: [image:1]", md_text)
