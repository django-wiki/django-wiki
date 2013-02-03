import markdown
import re

from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.template import Context

MACRO_RE = re.compile(r'.*(\[(?P<macro>\w+)(?P<kwargs>\s\w+\:.+)*\]).*', re.IGNORECASE)
KWARG_RE = re.compile(r'([^ |:]+):([^ |$]+)', re.IGNORECASE)

from wiki.plugins.macros import settings

class MacroExtension(markdown.Extension):
    """ Macro plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md, md_globals):
        """ Insert MacroPreprocessor before ReferencePreprocessor. """
        md.preprocessors.add('dw-macros', MacroPreprocessor(md), '>html_block')


class MacroPreprocessor(markdown.preprocessors.Preprocessor):
    """django-wiki macro preprocessor - parse text for various [some_macro] and 
    [some_macro (kw:arg)*] references. """
    
    allowed_methods = settings.METHODS
    
    def run(self, lines):
        new_text = []
        for line in lines:
            m = MACRO_RE.match(line)
            if m:
                macro = m.group('macro').strip()
                if not macro in MacroPreprocessor.allowed_methods:
                    continue
                kwargs = m.group('kwargs')
                if kwargs:
                    kwargs = eval('{' + KWARG_RE.sub(r'"\1":"\2",', kwargs) + '}')
                    line = getattr(self, macro)(**kwargs)
                else:
                    line = getattr(self, macro)()
            if not line is None:
                new_text.append(line)
        return new_text

    def article_list(self, depth=2):
        html = render_to_string(
            "wiki/plugins/macros/article_list.html",
            Context({
                'article_children': self.markdown.article.get_children,
                'depth': int(depth) + 1,
            })
        )
        return self.markdown.htmlStash.store(html, safe=True)
    article_list.meta = dict(
        short_description = _(u'Article list'),
        help_text = _(u'Insert a list of articles in this level.'),
        example_code = _(u'[article_list:depth=2]'),
        args = {'depth': _('Maximum depth to show levels for.')}
    )
