from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import settings

from wiki import managers
from wiki.models.pluginbase import ReusablePlugin
from wiki.models.article import BaseRevisionMixin

class IllegalFileExtension(Exception):
    """File extension on upload is not allowed"""
    pass

class Attachment(ReusablePlugin):

    objects = managers.ArticleFkManager()

    current_revision = models.OneToOneField('AttachmentRevision', 
                                            verbose_name=_(u'current revision'),
                                            blank=True, null=True, related_name='current_set',
                                            help_text=_(u'The revision of this attachment currently in use (on all articles using the attachment)'),
                                            )
    
    original_filename = models.CharField(max_length=256, verbose_name=_(u'original filename'), blank=True, null=True)

    def can_write(self, **kwargs):
        user = kwargs.get('user', None)
        if not settings.ANONYMOUS and (not user or user.is_anonymous()):
            return False
        return ReusablePlugin.can_write(self, **kwargs)
    
    def can_delete(self, user):
        return self.can_write(user=user)
    
    class Meta:
        verbose_name = _(u'attachment')
        verbose_name_plural = _(u'attachments')
        app_label = settings.APP_LABEL 
    
    def __unicode__(self):
        return "%s: %s" % (self.article.current_revision.title, self.original_filename)    
        
def upload_path(instance, filename):
    from os import path
    try:
        extension = filename.split(".")[-1]
    except IndexError:
        # No extension
        raise IllegalFileExtension("No file extension found in filename. That's not okay!")
    
    # Must be an allowed extension
    if not extension.lower() in map(lambda x: x.lower(), settings.FILE_EXTENSIONS):
        raise IllegalFileExtension("The following filename is illegal: %s. Extension has to be one of %s" % 
                                   (filename, ", ".join(settings.FILE_EXTENSIONS)))

    # Has to match original extension filename
    if instance.id and instance.attachment and instance.attachment.original_filename:
        original_extension = instance.attachment.original_filename.split(".")[-1]
        if not extension.lower() == original_extension:
            raise IllegalFileExtension("File extension has to be '%s', not '%s'." %
                                       (original_extension, extension.lower()))
    elif instance.attachment:
        instance.attachment.original_filename = filename
        
    upload_path = settings.UPLOAD_PATH
    upload_path = upload_path.replace('%aid', str(instance.attachment.article.id))
    if settings.UPLOAD_PATH_OBSCURIFY:
        import random, hashlib
        m=hashlib.md5(str(random.randint(0,100000000000000)))
        upload_path = path.join(upload_path, m.hexdigest())
    return path.join(upload_path, filename + '.upload')


class AttachmentRevision(BaseRevisionMixin, models.Model):
    
    attachment = models.ForeignKey('Attachment')

    file = models.FileField(upload_to=upload_path, #@ReservedAssignment
                            max_length=255,
                            verbose_name=_(u'file'),
                            storage=settings.STORAGE_BACKEND)
        
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _(u'attachment revision')
        verbose_name_plural = _(u'attachment revisions')
        ordering = ('created',)
        get_latest_by = ('revision_number',)
        app_label = settings.APP_LABEL
        
    def get_filename(self):
        """Used to retrieve the filename of a revision.
        But attachment.original_filename should always be used in the frontend
        such that filenames stay consistent."""
        # TODO: Perhaps we can let file names change when files are replaced?
        if not self.file:
            return None
        filename = self.file.name.split("/")[-1]
        return ".".join(filename.split(".")[:-1])
    
    def get_size(self):
        """Used to retrieve the file size and not cause exceptions."""
        try:
            return self.file.size
        except OSError:
            return None
        except ValueError:
            return None
    
    def save(self, *args, **kwargs):
        if (not self.id and
            not self.previous_revision and 
            self.attachment and
            self.attachment.current_revision and 
            self.attachment.current_revision != self):
            
            self.previous_revision = self.attachment.current_revision

        if not self.revision_number:
            try:
                previous_revision = self.attachment.attachmentrevision_set.latest()
                self.revision_number = previous_revision.revision_number + 1
            # NB! The above should not raise the below exception, but somehow it does.
            except AttachmentRevision.DoesNotExist, Attachment.DoesNotExist:
                self.revision_number = 1
        
        super(AttachmentRevision, self).save(*args, **kwargs)
        
        if not self.attachment.current_revision:
            # If I'm saved from Django admin, then article.current_revision is me!
            self.attachment.current_revision = self
            self.attachment.save()

    def __unicode__(self):
        return "%s: %s (r%d)" % (self.attachment.article.current_revision.title, 
                                 self.attachment.original_filename,
                                 self.revision_number)    
