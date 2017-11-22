# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import markdown
from django.template.loader import render_to_string
from wiki.plugins.images import models, settings

IMAGE_RE = re.compile(
    r'.*(\[image\:(?P<id>[0-9]+)(\s+align\:(?P<align>right|left))?(\s+size\:(?P<size>default|small|medium|large|orig))?\s*\]).*',
    re.IGNORECASE)


class ImageExtension(markdown.Extension):

    """ Images plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md, md_globals):
        """ Insert ImagePreprocessor before ReferencePreprocessor. """
        md.preprocessors.add('dw-images', ImagePreprocessor(md), '>html_block')
        md.postprocessors.add('dw-images-cleanup', ImagePostprocessor(md), '>raw_html')


class ImagePreprocessor(markdown.preprocessors.Preprocessor):
    """
    django-wiki image preprocessor
    Parse text for [image:id align:left|right|center] references.

    For instance:

    [image:id align:left|right|center]
        This is the caption text maybe with [a link](...)

    So: Remember that the caption text is fully valid markdown!
    """

    def run(self, lines):  # NOQA
        new_text = []
        previous_line = ""
        line_index = None
        previous_line_was_image = False
        image = None
        image_id = None
        alignment = None
        size = settings.THUMBNAIL_SIZES['default']
        caption_lines = []
        for line in lines:
            m = IMAGE_RE.match(line)
            if m:
                previous_line_was_image = True
                image_id = m.group('id').strip()
                alignment = m.group('align')
                if m.group('size'):
                    size = settings.THUMBNAIL_SIZES[m.group('size')]
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
                    width = size.split("x")[0] if size else None
                    html = render_to_string(
                        "wiki/plugins/images/render.html",
                        context={
                            'image': image,
                            'caption': caption_placeholder,
                            'align': alignment,
                            'size': size,
                            'width': width
                        })
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


class ImagePostprocessor(markdown.postprocessors.Postprocessor):

    def run(self, text):
        """
        This cleans up after Markdown's well-intended placing of image tags
        inside <p> elements. The problem is that Markdown should put
        <p> tags around images as they are inline elements. However, because
        we wrap them in <figure>, we don't actually want it and have to
        remove it again after.
        """
        text = text.replace("<p><figure", "<figure")
        text = text.replace("</figure>\n</p>", "</figure>")
        return text
