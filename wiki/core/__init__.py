import markdown

from wiki.conf import settings


class ArticleMarkdown(markdown.Markdown):
    
    def __init__(self, article, *args, **kwargs):
        kwargs['safe_mode'] = settings.MARKDOWN_SAFE_MODE 
        markdown.Markdown.__init__(self, *args, **kwargs)
        self.article = article

def article_markdown(text, article, *args, **kwargs):
    md = ArticleMarkdown(article, *args, **kwargs)
    return md.convert(text)
