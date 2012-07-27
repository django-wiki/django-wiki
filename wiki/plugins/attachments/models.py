from django.db import models
from django.utils.translation import ugettext_lazy as _

import settings

from wiki.conf import settings as wiki_settings
from wiki.models.pluginbase import ReusablePlugin
from wiki.models.article import BaseRevision

class IllegalFileExtension(Exception):
    """File extension on upload is not allowed"""
    pass

class Attachment(ReusablePlugin):
    
    current_revision = models.OneToOneField('AttachmentRevision', 
                                            verbose_name=_(u'current revision'),
                                            blank=True, null=True, related_name='current_set',
                                            help_text=_(u'The revision of this attachment currently in use (on all articles using the attachment)'),
                                            )

    class Meta:
        verbose_name = _(u'attachment')
        verbose_name_plural = _(u'attachments')
        app_label = wiki_settings.APP_LABEL
        
def upload_path(instance, filename):
    from os import path
    try:
        extension = filename.split(".")[-1]
    except IndexError:
        raise IllegalFileExtension()
    if not extension.lower() in map(lambda x: x.lower(), settings.FILE_EXTENTIONS):
        raise IllegalFileExtension()
    upload_path = settings.UPLOAD_PATH
    upload_path = upload_path.replace('%aid', str(instance.original_article.id))
    if settings.UPLOAD_PATH_OBSCURIFY:
        import random, hashlib
        m=hashlib.md5(str(random.randint(0,100000000000000)))
        upload_path = path.join(upload_path, m.hexdigest())
    return path.join(upload_path, filename + '.upload')
        
class AttachmentRevision(BaseRevision):
    
    attachment = models.ForeignKey('Attachment')

    file = models.FileField(upload_to=upload_path, #@ReservedAssignment
                            verbose_name=_(u'file'))
    
    original_filename = models.CharField(max_length=256, verbose_name=_(u'original filename'))
    
    overwritten = models.BooleanField(default=False)

    class Meta:
        verbose_name = _(u'attachment revision')
        verbose_name_plural = _(u'attachment revisions')
        get_latest_by = ('revision_number',)
        app_label = wiki_settings.APP_LABEL
