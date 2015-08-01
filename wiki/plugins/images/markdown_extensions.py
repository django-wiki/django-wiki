from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import markdown
import re

from django.template.loader import render_to_string
from django.template import Context

IMAGE_RE = re.compile(
    r'.*(\[image\:(?P<id>\d+)(\s+align\:(?P<align>right|left))?\s*\]).*',
    re.IGNORECASE)

from wiki.plugins.images import models


class ImageExtension(markdown.Extension):

    """ Images plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md, md_globals):
        """ Insert ImagePreprocessor before ReferencePreprocessor. """
        md.preprocessors.add('dw-images', ImagePreprocessor(md), '>html_block')


class ImagePreprocessor(markdown.preprocessors.Preprocessor):

    """django-wiki image preprocessor - parse text for [image:id align:left|right|center] references. """

    def run(self, lines):
        new_text = []
        previous_line = ""
        line_index = None
        previous_line_was_image = False
        image = None
        image_id = None
        alignment = None
        caption_lines = []
        for line in lines:
            m = IMAGE_RE.match(line)
            if m:
                previous_line_was_image = True
                image_id = m.group('id').strip()
                alignment = m.group('align')
                try:
                    image = models.Image.objects.get(
                        article=self.markdown.article,
                        id=image_id,
                        current_revision__deleted=False)
                except models.Image.DoesNotExist:
                    pass
                line_index = line.find(m.group(1))
                line = line.replace(m.group(1), "")
                previous_line = line
                caption_lines = []
            elif previous_line_was_image:
                if line.startswith("    "):
                    caption_lines.append(line[4:])
                    line = None
                else:
                    caption_placeholder = "{{{IMAGECAPTION}}}"
                    html = render_to_string(
                        "wiki/plugins/images/render.html",
                        Context(
                            {'image': image, 'caption': caption_placeholder,
                             'align': alignment}))
                    html_before, html_after = html.split(caption_placeholder)
                    placeholder_before = self.markdown.htmlStash.store(
                        html_before,
                        safe=True)
                    placeholder_after = self.markdown.htmlStash.store(
                        html_after,
                        safe=True)
                    new_line = placeholder_before + "\n".join(
                        caption_lines) + placeholder_after + "\n"
                    previous_line_was_image = False
                    if previous_line is not "":
                        if previous_line[line_index:] is not "":
                            new_line = new_line[0:-1]
                        new_text[-1] = (previous_line[0:line_index] +
                                        new_line +
                                        previous_line[line_index:] +
                                        "\n" +
                                        line)
                        line = None
                    else:
                        line = new_line + line
            if line is not None:
                new_text.append(line)
        return new_text
