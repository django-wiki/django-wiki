# -*- coding: utf-8 -*-
import markdown
import re

# from django.template.loader import render_to_string
# from django.template import Context

IMAGE_RE = re.compile(r'{{(?P<template_title>.+?)}}')

from wiki.plugins.template import models


class TemplateExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """ Insert ImagePreprocessor before ReferencePreprocessor. """
        md.preprocessors.add(
            'insert-template', TemplatePreprocessor(md), '>html_block')


class TemplatePreprocessor(markdown.preprocessors.Preprocessor):

    def run(self, lines):
        new_text = []
        template_cache = dict(
            models.Template.objects.filter(
                articles=self.markdown.article
            ).values_list('template_title', 'current_revision__template_content')
        )
        for line in lines:
            if IMAGE_RE.search(line):
                template_titles = IMAGE_RE.findall(line)
                for title in template_titles:
                    if title in template_cache:
                        line = line.replace(
                            "{{%s}}" % title, template_cache[title])
            new_text.append(line)
        return new_text

        # new_text = []
        # previous_line_was_image = False
        # image = None
        # image_id = None
        # alignment = None
        # caption_lines = []
        # for line in lines:
        #     m = IMAGE_RE.match(line)
        #     if m:
        #         previous_line_was_image = True
        #         image_id = m.group('id').strip()
        #         alignment = m.group('align')
        #         try:
        #             image = models.Image.objects.get(article=self.markdown.article,
        #                                             id=image_id,
        #                                             current_revision__deleted=False)
        #         except models.Image.DoesNotExist:
        #             pass
        #         line = line.replace(m.group(1), "")
        #         caption_lines = []
        #     elif previous_line_was_image:
        #         if line.startswith("    "):
        #             caption_lines.append(line[4:])
        #             line = None
        #         else:
        #             caption_placeholder = "{{{IMAGECAPTION}}}"
        #             html = render_to_string("wiki/plugins/images/render.html",
        #                                     Context({'image': image,
        #                                              'caption': caption_placeholder,
        #                                              'align': alignment}))
        #             html_before, html_after = html.split(caption_placeholder)
        #             placeholder_before = self.markdown.htmlStash.store(html_before, safe=True)
        #             placeholder_after = self.markdown.htmlStash.store(html_after, safe=True)
        #             line = placeholder_before + "\n".join(caption_lines) + placeholder_after + "\n" + line
        #             previous_line_was_image = False
        #     if not line is None:
        #         new_text.append(line)
        # return new_text
