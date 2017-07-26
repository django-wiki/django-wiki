import markdown
import re

from django.template.loader import render_to_string
from django.template import Context
from wiki.core import article_markdown

IMAGE_RE = re.compile(r'.*(\[image\:(?P<id>\d+)\s+align\:(?P<align>right|left|center)\s*\]).*',
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
                alignment = m.group('align').strip()
                try:
                    image = models.Image.objects.get(article=self.markdown.article,
                                                    id=image_id,
                                                    current_revision__deleted=False)
                except models.Image.DoesNotExist:
                    pass
                line = line.replace(m.group(1), "")
            elif previous_line_was_image:
                if line.startswith("    "):
                    caption_lines.append(line[4:])
                    line = None
                else:
                    html = render_to_string(
                        "wiki/plugins/images/render.html",
                        context={
                            'image': image,
                            'caption': article_markdown("\n".join(caption_lines),
                                                        self.markdown.article,
                                                        extensions=self.markdown.registeredExtensions),
                            'align': alignment
                        }
                    )
                    line = html + line
                    previous_line_was_image = False
            if not line is None:
                new_text.append(line)
        return new_text
    
