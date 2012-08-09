import markdown
import re

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

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
                attachment = models.Attachment.objects.get(article=self.markdown.article,
                                                           id=attachment_id)
                url = reverse('wiki:attachments_download', kwargs={'article_id': self.markdown.article.id,
                                                                   'attachment_id':attachment.id,})
                line = line.replace(m.group(1), u"""<span class="attachment"><a href="%s" title="%s">%s</a>""" % 
                                    (url, _(u"Click to download file"), attachment.original_filename))
            new_text.append(line)
        return new_text
    
