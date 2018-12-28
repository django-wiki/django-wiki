import markdown
import bleach

class ArticleMarkdown(markdown.Markdown):

    def __init__(self, article, *args, **kwargs):
        markdown.Markdown.__init__(self, *args, **kwargs)
        self.article = article


def article_markdown(text, article, *args, **kwargs):
    md = ArticleMarkdown(article, *args, **kwargs)
    text = bleach.clean(text, strip=True)
    return md.convert(text)
