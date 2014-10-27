# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import markdown
import re

from wiki.plugins.template.models import Template

TEMPLATE_RE = r"((?:^[^ \t].* )?){{(?P<title>(?:%s)(?:\|[^}]+)*)}}((?: .+)|$)"


class TemplateExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """ Insert TemplatePreprocessor before ReferencePreprocessor. """
        md.preprocessors.add(
            'insert-template',
            TemplatePreprocessor(md),
            '>html_block'
        )


class TemplatePreprocessor(markdown.preprocessors.Preprocessor):

    def run(self, lines):
        new_text = []
        template_cache = dict(
            Template.objects.filter(
                articles=self.markdown.article,
                current_revision__deleted=False,
            ).values_list(
                'template_title',
                'current_revision__template_content'
            )
        )
        RE_TEXT = TEMPLATE_RE % "|".join(template_cache.keys())
        fenced_code_block = False

        # This function replaces the template parameters and generate content.
        def gen_content(tag_split):
            content = template_cache[tag_split[0]]
            vals = tag_split[1:]
            for i, val_str in enumerate(vals):
                val_split = val_str.split("=")
                if len(val_split) >= 2:
                    val_name = val_split[0]
                    val = val_split[1]
                elif len(val_split) == 1:
                    val_name = str(i)
                    val = val_split[0]
                else:
                    val_name = str(i)
                    val = ""
                val_tag = "{{{%s}}}" % val_name
                content = content.replace(val_tag, val)
            return content

        for line in lines:
            if (line.startswith("```") or line.startswith("~~~")
                    and not fenced_code_block):
                new_text.append(line)
                fenced_code_block = True
                continue
            if fenced_code_block and line.startswith("```"):
                new_text.append(line)
                fenced_code_block = False
                continue
            if fenced_code_block:
                new_text.append(line)
                continue
            m = re.match(RE_TEXT, line)
            while m:
                template_tag = re.findall(RE_TEXT, line)[0][1].split("|")
                content = gen_content(template_tag).replace(
                    "{{", "\u0018-\u0018"
                ).replace(
                    "}}", "\u0018+\u0018"
                )
                sub_line = r"\1{0}\3".format(content)
                line = re.sub(RE_TEXT, sub_line, line)
                m = re.match(RE_TEXT, line)
            line = line.replace(
                "\u0018-\u0018", "{{"
            ).replace(
                "\u0018+\u0018", "}}"
            )
            new_text.append(line)
        return new_text
