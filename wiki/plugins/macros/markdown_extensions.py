# -*- coding: utf-8 -*-
import markdown
import re

from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.template import Context

# See: http://stackoverflow.com/questions/430759/regex-for-managing-escaped-characters-for-items-like-string-literals
re_sq_short = r"'([^'\\]*(?:\\.[^'\\]*)*)'"

MACRO_RE = re.compile(r'.*(\[(?P<macro>\w+)(?P<kwargs>\s\w+\:.+)*\]).*', re.IGNORECASE)
KWARG_RE = re.compile(r'\s*(?P<arg>\w+)(:(?P<value>([^\']+|%s)))?' % re_sq_short, re.IGNORECASE)

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
        # Look at all those indentations.
        # That's insane, let's get a helper library
        # Please note that this pattern is also in plugins.images
        new_text = []
        for line in lines:
            m = MACRO_RE.match(line)
            if m:
                macro = m.group('macro').strip()
                if macro in MacroPreprocessor.allowed_methods:
                    kwargs = m.group('kwargs')
                    if kwargs:
                        kwargs_dict = {}
                        for kwarg in KWARG_RE.finditer(kwargs):
                            arg = kwarg.group('arg')
                            value = kwarg.group('value')
                            if value is None:
                                value = True
                            if isinstance(value, basestring):
                                # If value is enclosed with ': Remove and remove escape sequences
                                if value.startswith(u"'") and len(value) > 2:
                                    value = value[1:-1]
                                    value = value.replace(u"\\\\", u"¤KEEPME¤")
                                    value = value.replace(u"\\", u"")
                                    value = value.replace(u"¤KEEPME¤", u"\\")
                            kwargs_dict[arg] = value
                        line = getattr(self, macro)(**kwargs_dict)
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
        example_code = _(u'[article_list depth:2]'),
        args = {'depth': _('Maximum depth to show levels for.')}
    )
