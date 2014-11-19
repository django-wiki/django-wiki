# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import markdown
import re
from six import string_types

from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.template import Context

#
# Some general RE
# See: http://stackoverflow.com/questions/430759/regex-for-managing-escaped-characters-for-items-like-string-literals
#
# Unquoted string without escaped characters
uq_re = r"""[^'"\s\]][^\s\]]*"""
# Single quoted string with escaped characters
sq_re = r"""'([^'\\]*(?:\\.[^'\\]*)*)'"""
# Double quoted string with escaped characters
dq_re = r'''"([^"\\]*(?:\\.[^"\\]*)*)"'''

#
# Macro specific RE
#
# Name of the macro
name_re = r"""\w+"""
# Name of an optional argument
arg_re = r"""\w+"""
# Value of an optional argument: one_word or 'several words' or "multiple words"
value_re = r"""%s|%s|%s""" % (uq_re, sq_re, dq_re)
# Optional argument as name:value
kwarg_re = r"""(%s)\s*:\s*(%s)""" % (arg_re, value_re)
# A list of optional arguments
kwargs_re = r"""(\s+%s)*""" % (kwarg_re,)
# RE for the whole macro
MACRO_RE = re.compile(r"""\[\s*(?P<macro>%s)(?P<kwargs>%s)\s*\]""" % (name_re, kwargs_re), re.IGNORECASE)
# RE for an optional argument name:value
KWARG_RE = re.compile(r"""\s*(?P<arg>%s)\s*:\s*(?P<value>%s)\s*""" % (arg_re, value_re), re.IGNORECASE)


from wiki.plugins.macros import settings

class MacroExtension(markdown.Extension):
    """ Macro plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md, md_globals):
        """ Insert MacroPreprocessor before ReferencePreprocessor. """
        md.preprocessors.add('dw-macros', MacroPreprocessor(md), '>html_block')


class MacroPreprocessor(markdown.preprocessors.Preprocessor):
    """django-wiki macro preprocessor - parse text for various [some_macro] and 
    [some_macro (kw:arg)*] references. """
    
    def run(self, lines):
        # Look at all those indentations.
        # That's insane, let's get a helper library
        # Please note that this pattern is also in plugins.images
        new_text = []
        for line in lines:
            new_line = ""
            pos = 0
            for m in MACRO_RE.finditer(line):
                new_line += line[pos:m.start()]
                pos = m.end()
                macro = m.group('macro').strip()
                if macro in settings.METHODS and hasattr(self, macro):
                    kwargs = m.group('kwargs')
                    if kwargs:
                        kwargs_dict = {}
                        for kwarg in KWARG_RE.finditer(kwargs):
                            arg = kwarg.group('arg')
                            value = kwarg.group('value')
                            if value is None:
                                value = True
                            if isinstance(value, string_types):
                                # If value is enclosed with ': Remove and remove escape sequences
                                if (value.startswith("'") or value.startswith('"')) and len(value) > 2:
                                    value = value[1:-1]
                                    value = value.replace("\\\\", "¤KEEPME¤")
                                    value = value.replace("\\", "")
                                    value = value.replace("¤KEEPME¤", "\\")
                            kwargs_dict[str(arg)] = value
                        try:
                            new_line += getattr(self, macro)(**kwargs_dict)
                        except TypeError:
                            # Catch invalid args
                            new_line += line[m.start():m.end()]
                        except ValueError:
                            # Catch invalid values
                            new_line += line[m.start():m.end()]
                    else:
                        new_line += getattr(self, macro)()
                        
            if not line is None:
                if pos != 0:
                    new_line += line[pos:]
                    line = new_line
                new_text.append(line)
        return new_text

    def article_list(self, depth="2", title=_("Article index")):
        html = render_to_string(
            "wiki/plugins/macros/article_list.html",
            Context({
                'article_children': self.markdown.article.get_children(article__current_revision__deleted=False),
                'depth': int(depth) + 1,
                'title': title,
            })
        )
        return self.markdown.htmlStash.store(html, safe=True)
    article_list.meta = dict(
        short_description = _('Article list'),
        help_text = _('Insert a list of articles in this level.'),
        example_code = _('[article_list depth:2 title:\'My list\']'),
        args = {'depth': _('Maximum depth to show levels for.'),
                'title': _('Title for the list.'),}
    )

    def toc(self):
        return "[TOC]"
    toc.meta = dict(
        short_description = _('Table of contents'),
        help_text = _('Insert a table of contents matching the headings.'),
        example_code = _('[TOC]'),
        args = {}
    )

    def wikilink(self):
        return ""
    wikilink.meta = dict(
        short_description = _('WikiLinks'),
        help_text = _('Insert a link to another wiki page with a short notation.'),
        example_code = _('[[WikiLink]]'),
        args = {}
    )
