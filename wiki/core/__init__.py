import markdown

class ArticleMarkdown(markdown.Markdown):
    
    def __init__(self, article, *args, **kwargs):
        kwargs['safe_mode'] = "remove"
        markdown.Markdown.__init__(self, *args, **kwargs)
        self.article = article

def article_markdown(text, article, *args, **kwargs):
    md = ArticleMarkdown(article, *args, **kwargs)
    return md.convert(text)
