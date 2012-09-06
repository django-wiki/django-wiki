import markdown
import re

from django.core.urlresolvers import reverse
from django.template.context import Context
from django.template.loader import render_to_string

ATTACHMENT_RE = re.compile(r'.*(\[attachment\:(?P<id>\d+)\]).*', re.IGNORECASE)

from wiki.plugins.attachments import models

class AttachmentExtension(markdown.Extension):
    """ Abbreviation Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Insert AbbrPreprocessor before ReferencePreprocessor. """
        md.preprocessors.add('dw-attachments', AttachmentPreprocessor(md), '>html_block')

class AttachmentPreprocessor(markdown.preprocessors.Preprocessor):
    """django-wiki attachment preprocessor - parse text for [attachment:id] references. """

    def run(self, lines):
        new_text = []
        for line in lines:
            m = ATTACHMENT_RE.match(line)
            if m:
                attachment_id = m.group('id').strip()
                try:
                    attachment = models.Attachment.objects.get(articles=self.markdown.article,
                                                               id=attachment_id, current_revision__deleted=False)
                    url = reverse('wiki:attachments_download', kwargs={'article_id': self.markdown.article.id,
                                                                       'attachment_id':attachment.id,})
                    html = render_to_string("wiki/plugins/attachments/render.html",
                                            Context({'url': url, 
                                                     'filename': attachment.original_filename,}))
                    line = self.markdown.htmlStash.store(html, safe=True)
                except models.Attachment.DoesNotExist:
                    line = line.replace(m.group(1), u"""<span class="attachment attachment-deleted">Attachment with ID #%s is deleted.</span>""" % attachment_id)                    
            new_text.append(line)
        return new_text
    
