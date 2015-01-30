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
            'dw-template',
            TemplatePreprocessor(md),
            '>html_block'
        )


class TemplatePreprocessor(markdown.preprocessors.Preprocessor):

    def run(self, lines):
        new_text = []
        template_cache = dict(
            Template.get_by_article(self.markdown.article).values_list(
                'template_title',
                'current_revision__template_content'
            )
        )
        RE_TEXT = TEMPLATE_RE % "|".join(template_cache.keys())
        fenced_code_block = False

        # This function replaces the template parameters and generate content.
        def gen_content(template_tag):
            tag_split = template_tag.split("|")
            content = template_cache[tag_split[0]]
            for i, val_str in enumerate(tag_split[1:]):
                val_split = val_str.split("=")
                val_tag = "{{{%s}}}" % i
                if re.match(r"'.*'", val_str) or re.match(r'".*"', val_str):
                    # one string value
                    val = val_str[1:-1]
                elif len(val_split) > 2:
                    val = "=".join(val_split[1:])
                    if re.match(r"'.*'", val) or re.match(r'".*"', val):
                        # like: title="Title blah blah"
                        val_tag = "{{{%s}}}" % val_split[0]
                        val = val[1:-1]
                    else:
                        # one string value
                        val = val_str
                elif len(val_split) == 2:
                    # like: color=blue
                    val_tag = "{{{%s}}}" % val_split[0]
                    val = val_split[1]
                elif len(val_split) == 1:
                    # one string value
                    val = val_split[0]
                else:
                    # empty string value
                    val = ""
                if re.match(r"'.*'", val) or re.match(r'".*"', val):
                    val = val[1:-1]
                content = content.replace(val_tag, val)
            return content

        block_template_lines = []
        block_template_on = False
        for line in lines:
            matched = False
            if (line.startswith("```") or line.startswith("~~~")
                    and not fenced_code_block):
                new_text.append(line)
                fenced_code_block = True
                continue
            if fenced_code_block and (line.startswith("```") or line.startswith("~~~")):
                new_text.append(line)
                fenced_code_block = False
                continue
            if fenced_code_block:
                new_text.append(line)
                continue
            if line.startswith("{{") and not "}}" in line and not block_template_on:
                block_template_lines.append(line)
                block_template_on = True
                continue
            if block_template_on:
                block_template_lines.append(line)
                if line == "}}":
                    block_template_on = False
                    line = "".join(block_template_lines)
                    block_template_lines = []
                else:
                    continue
            m = re.match(RE_TEXT, line)
            while m:
                matched = True
                template_tag = re.findall(RE_TEXT, line)[0][1]
                # if "{{" or "}}" in content, replace it!
                # cause may template content has "{{" or "}}",
                # should not be transform at next loop
                content = gen_content(template_tag).replace(
                    "{{", "\u0018-\u0018"
                ).replace(
                    "}}", "\u0018+\u0018"
                )
                line = re.sub(
                    RE_TEXT,
                    lambda x: x.group(1)+content+x.group(3),
                    line
                )
                m = re.match(RE_TEXT, line)
            # finally, replace back.
            line = line.replace(
                "\u0018-\u0018", "{{"
            ).replace(
                "\u0018+\u0018", "}}"
            )
            # Doesn't support mixed markdown and html
            if matched and ("</" in line or "/>" in line):
                line = self.markdown.htmlStash.store(line, safe=True)
            new_text.append(line)
        return new_text
