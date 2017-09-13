# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
import itertools
import markdown
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from six import string_types
from .. import settings
from .. import utils

# See:
# http://stackoverflow.com/questions/430759/regex-for-managing-escaped-characters-for-items-like-string-literals
re_sq_short = r"'([^'\\]*(?:\\.[^'\\]*)*)'"

MACRO_RE = re.compile(
    r'(?P<prefix>.*?)\[\s*(?P<cmd>(input|get))(-(?P<variant>\w+))?(?P<kwargs>(\s+[-a-z0-9_./]+?(\:.+?)?)*?)\](?P<suffix>.*)$',
    re.IGNORECASE
)

KWARG_RE = re.compile(
    r'\s*(?P<arg>[-a-z0-9_./]+)(:(?P<value>([^\'\s]+|%s)))?' %
    re_sq_short,
    re.IGNORECASE)


class InputExtension(markdown.Extension):

    """ Input plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md, md_globals):
        """ Insert InputPreprocessor before ReferencePreprocessor. """
        md.preprocessors.add('dw-input', InputPreprocessor(md), '>html_block')



class InputPreprocessor(markdown.preprocessors.Preprocessor):

    """django-wiki input preprocessor - parse text for various [some_macro] and
    [some_macro (kw:arg)*] references. """
    def __init__(self, *args, **kwargs):
        super(InputPreprocessor, self).__init__(*args, **kwargs)
        self.input_names = set()

        if self.markdown:
            self.markdown.inputextension_fields = dict()


    def process_args(self, args, **kwargs):
        for m in KWARG_RE.finditer(args):
            arg = m.group('arg')
            value = m.group('value')

            if value is None:
                kwargs[arg] = None
            elif isinstance(value, string_types):
                # If value is enclosed with ': Remove and
                # remove escape sequences
                if value.startswith("'") and len(value) > 2:
                    value = value[1:-1]
                    value = value.replace("\\\\", "¤KEEPME¤")
                    value = value.replace("\\", "")
                    value = value.replace("¤KEEPME¤", "\\")
                kwargs[arg] = value

        return kwargs


    def process_line(self, line):
        m = MACRO_RE.match(line)
        if not m:
            return line

        args = self.process_args(m.group('kwargs'))
        html = getattr(self, "cmd_" + m.group('cmd'))(m.group('variant'), args)

        out = m.group('prefix')
        out += self.markdown.htmlStash.store(html, safe=True)
        out += self.process_line(m.group('suffix'))

        return out


    def run(self, lines):
        return [self.process_line(l) for l in lines]


    def cmd_input(self, variant, args):
        if variant not in settings.INPUTS:
            variant = settings.INPUTS[0] if len(settings.INPUTS) else "text"

        for k in args:
            if args[k] is None:
                name = re.sub('[^-A-Za-z0-9_.]+', '', k)
                break
        else:
            for i in itertools.count():
                name = "input_{}".format(i)
                if i and name not in self.input_names:
                    break

        self.input_names.add(name)
        self.markdown.inputextension_fields[name] = variant

        return render_to_string(
            "wiki/plugins/inputs/input/{}.html".format(variant),
            context=dict(
                article=self.markdown.article,
                preview=self.markdown.preview,
                variant=variant,
                name=name,
            ),
        )

    cmd_input.meta = dict(
        short_description=_('Input Field'),
        help_text=_('Input text field.'),
        example_code='[input] or [input-type name]',
        args={
            'name': _('name of the input field.'),
            'type': _('type of the field: {}').format(", ".join(settings.INPUTS)),

        }
    )


    def cmd_get(self, variant, args):
        for k in args:
            field = utils.parse_input(self.markdown.article, k)
            if args[k] is None and field:
                break
        else:
            return "<b>!!</b>"

        return render_to_string(
            "wiki/plugins/inputs/get.html".format(variant),
            context=dict(
                name=field[1],
                path=field[0],
                preview=self.markdown.preview,
                variant=variant,
            )
        )

    cmd_get.meta = dict(
        short_description=_('Get Field'),
        help_text=_('Get a field value.'),
        example_code='[get name] or [get:type path/name] ',
        args={
            'type': _('<i>all</i> to get all variants of the field'),
            '[path/]name': _('name of the input to get'),
        }
    )


    # try:
    #     article = models.URLPath.get_by_path(path).article
    # except models.URLPath.DoesNotExist:
    #     continue
