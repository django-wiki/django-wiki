import markdown
from django.template.loader import render_to_string
from wiki.plugins.images import models, settings

IMAGE_RE = (
    r"(?:(?im)" +
    # Match '[image:N'
    r"\[image\:(?P<id>[0-9]+)" +
    # Match optional 'align'
    r"(?:\s+align\:(?P<align>right|left))?" +
    # Match optional 'size'
    r"(?:\s+size\:(?P<size>default|small|medium|large|orig))?" +
    # Match ']' and rest of line.
    # Normally [^\n] could be replaced with a dot '.', since '.'
    # does not match newlines, but inline processors run with re.DOTALL.
    r"\s*\](?P<trailer>[^\n]*)$" +
    # Match zero or more caption lines, each indented by four spaces.
    r"(?P<caption>(?:\n    [^\n]*)*))"
)


class ImageExtension(markdown.Extension):

    """ Images plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('dw-images', ImagePattern(IMAGE_RE, md), '>link')
        md.postprocessors.add('dw-images-cleanup', ImagePostprocessor(md), '>raw_html')


class ImagePattern(markdown.inlinepatterns.Pattern):
    """
    django-wiki image preprocessor
    Parse text for [image:N align:ALIGN size:SIZE] references.

    For instance:

    [image:id align:left|right]
        This is the caption text maybe with [a link](...)

    So: Remember that the caption text is fully valid markdown!
    """

    def handleMatch(self, m):
        image = None
        image_id = None
        alignment = None
        size = settings.THUMBNAIL_SIZES["default"]

        image_id = m.group("id").strip()
        alignment = m.group("align")
        if m.group("size"):
            size = settings.THUMBNAIL_SIZES[m.group("size")]
        try:
            image = models.Image.objects.get(
                article=self.markdown.article,
                id=image_id,
                current_revision__deleted=False,
            )
        except models.Image.DoesNotExist:
            pass

        caption = m.group("caption")
        trailer = m.group('trailer')

        caption_placeholder = "{{{IMAGECAPTION}}}"
        width = size.split("x")[0] if size else None
        html = render_to_string(
            "wiki/plugins/images/render.html",
            context={
                "image": image,
                "caption": caption_placeholder,
                "align": alignment,
                "size": size,
                "width": width,
            },
        )
        html_before, html_after = html.split(caption_placeholder)
        placeholder_before = self.markdown.htmlStash.store(html_before, safe=True)
        placeholder_after = self.markdown.htmlStash.store(html_after, safe=True)
        return placeholder_before + caption + placeholder_after + trailer


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
