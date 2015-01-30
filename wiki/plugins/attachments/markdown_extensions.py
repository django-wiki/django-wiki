from __future__ import unicode_literals
from __future__ import absolute_import
import markdown
import re

from django.core.urlresolvers import reverse
from django.template.context import Context
from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser
from wiki.core.permissions import can_read

ATTACHMENT_RE = re.compile(
    r'(?P<before>.*)(\[attachment\:(?P<id>\d+)\])(?P<after>.*)',
    re.IGNORECASE)

from wiki.plugins.attachments import models


class AttachmentExtension(markdown.Extension):

    """ Abbreviation Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Insert AbbrPreprocessor before ReferencePreprocessor. """
        md.preprocessors.add(
            'dw-attachments',
            AttachmentPreprocessor(md),
            '>html_block')


class AttachmentPreprocessor(markdown.preprocessors.Preprocessor):

    """django-wiki attachment preprocessor - parse text for [attachment:id] references. """

    def run(self, lines):
        new_text = []
        for line in lines:
            m = ATTACHMENT_RE.match(line)
            if m:
                attachment_id = m.group('id').strip()
                before = self.run([m.group('before')])[0]
                after = self.run([m.group('after')])[0]
                try:
                    attachment = models.Attachment.objects.get(
                        articles__current_revision__deleted=False,
                        id=attachment_id, current_revision__deleted=False,
                        articles=self.markdown.article
                    )
                    url = reverse(
                        'wiki:attachments_download',
                        kwargs={
                            'article_id': self.markdown.article.id,
                            'attachment_id': attachment.id,
                        })

                    # The readability of the attachment is decided relative
                    # to the owner of the original article.
                    # I.e. do not insert attachments in other articles that
                    # the original uploader cannot read, that would be out
                    # of scope!
                    article_owner = attachment.article.owner
                    if not article_owner:
                        article_owner = AnonymousUser()

                    attachment_can_read = can_read(
                        self.markdown.article, article_owner)
                    html = render_to_string(
                        "wiki/plugins/attachments/render.html",
                        Context({
                            'url': url,
                            'filename': attachment.original_filename,
                            'attachment_can_read': attachment_can_read,
                        }))
                    line = self.markdown.htmlStash.store(html, safe=True)
                except models.Attachment.DoesNotExist:
                    html = """<span class="attachment attachment-deleted">Attachment with ID #%s is deleted.</span>""" % attachment_id
                    line = line.replace(
                        m.group(2),
                        self.markdown.htmlStash.store(
                            html,
                            safe=True))
                line = before + line + after
            new_text.append(line)
        return new_text
