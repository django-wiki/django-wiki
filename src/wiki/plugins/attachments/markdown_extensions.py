import re

import markdown
from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.urls import reverse
from wiki.core.markdown import add_to_registry
from wiki.core.permissions import can_read
from wiki.plugins.attachments import models

ATTACHMENT_RE = re.compile(
    r"(?P<before>.*)\[( *((attachment\:(?P<id>[0-9]+))|(title\:\"(?P<title>[^\"]+)\")|(?P<size>size)))+\](?P<after>.*)",
    re.IGNORECASE,
)


class AttachmentExtension(markdown.Extension):

    """Abbreviation Extension for Python-Markdown."""

    def extendMarkdown(self, md):
        """Insert AbbrPreprocessor before ReferencePreprocessor."""

        add_to_registry(
            md.preprocessors,
            "dw-attachments",
            AttachmentPreprocessor(md),
            ">html_block",
        )


class AttachmentPreprocessor(markdown.preprocessors.Preprocessor):

    """django-wiki attachment preprocessor - parse text for [attachment:id] references."""

    def run(self, lines):
        new_text = []
        for line in lines:
            m = ATTACHMENT_RE.match(line)
            if not m:
                new_text.append(line)
                continue

            attachment_id = m.group("id").strip()
            title = m.group("title")
            size = m.group("size")
            before = self.run([m.group("before")])[0]
            after = self.run([m.group("after")])[0]
            try:
                attachment = models.Attachment.objects.get(
                    articles__current_revision__deleted=False,
                    id=attachment_id,
                    current_revision__deleted=False,
                    articles=self.markdown.article,
                )
                url = reverse(
                    "wiki:attachments_download",
                    kwargs={
                        "article_id": self.markdown.article.id,
                        "attachment_id": attachment.id,
                    },
                )

                # The readability of the attachment is decided relative
                # to the owner of the original article.
                # I.e. do not insert attachments in other articles that
                # the original uploader cannot read, that would be out
                # of scope!
                article_owner = attachment.article.owner
                if not article_owner:
                    article_owner = AnonymousUser()
                if not title:
                    title = attachment.original_filename
                if size:
                    size = attachment.current_revision.get_size()

                attachment_can_read = can_read(self.markdown.article, article_owner)
                html = render_to_string(
                    "wiki/plugins/attachments/render.html",
                    context={
                        "url": url,
                        "filename": attachment.original_filename,
                        "title": title,
                        "size": size,
                        "attachment_can_read": attachment_can_read,
                    },
                )
                line = self.markdown.htmlStash.store(html)
            except models.Attachment.DoesNotExist:
                html = (
                    """<span class="attachment attachment-deleted">Attachment with ID """
                    """#{} is deleted.</span>"""
                ).format(attachment_id)
                line = line.replace(
                    "[" + m.group(2) + "]", self.markdown.htmlStash.store(html)
                )
            new_text.append(before + line + after)
        return new_text
