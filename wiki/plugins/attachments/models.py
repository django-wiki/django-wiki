# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os.path

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from . import settings

from wiki import managers
from wiki.models.pluginbase import ReusablePlugin
from wiki.models.article import BaseRevisionMixin
from django.db.models import signals
from six.moves import map
from six.moves import zip

class IllegalFileExtension(Exception):
    """File extension on upload is not allowed"""
    pass

class Attachment(ReusablePlugin):

    objects = managers.ArticleFkManager()

    current_revision = models.OneToOneField(
        'AttachmentRevision', 
        verbose_name=_('current revision'),
        blank=True, null=True, related_name='current_set',
        help_text=_('The revision of this attachment currently in use (on all articles using the attachment)'),
    )
    
    original_filename = models.CharField(max_length=256, verbose_name=_('original filename'), blank=True, null=True)

    def can_write(self, user):
        if not settings.ANONYMOUS and (not user or user.is_anonymous()):
            return False
        return ReusablePlugin.can_write(self, user)
    
    def can_delete(self, user):
        return self.can_write(user)
    
    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')
        app_label = settings.APP_LABEL 
    
    def __unicode__(self):
        return "%s: %s" % (self.article.current_revision.title, self.original_filename)    

def extension_allowed(filename):
    try:
        extension = filename.split(".")[-1]
    except IndexError:
        # No extension
        raise IllegalFileExtension("No file extension found in filename. That's not okay!")
    if not extension.lower() in map(lambda x: x.lower(), settings.FILE_EXTENSIONS):
        raise IllegalFileExtension("The following filename is illegal: %s. Extension has to be one of %s" % 
                                   (filename, ", ".join(settings.FILE_EXTENSIONS)))
    
    return extension
    
def upload_path(instance, filename):
    from os import path
    
    extension = extension_allowed(filename)
    
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
        import uuid
        upload_path = os.path.join(upload_path, uuid.uuid4().hex)
        
    if settings.APPEND_EXTENSION:
        filename += '.upload'
    return path.join(upload_path, filename)


class AttachmentRevision(BaseRevisionMixin, models.Model):
    
    attachment = models.ForeignKey('Attachment')

    file = models.FileField(upload_to=upload_path, #@ReservedAssignment
                            max_length=255,
                            verbose_name=_('file'),
                            storage=settings.STORAGE_BACKEND)
        
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _('attachment revision')
        verbose_name_plural = _('attachment revisions')
        ordering = ('created',)
        get_latest_by = 'revision_number'
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
            except AttachmentRevision.DoesNotExist as noattach: 
                Attachment.DoesNotExist = noattach
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


def on_revision_delete(instance, *args, **kwargs):
    if not instance.file:
        return
    
    # Remove file
    path = instance.file.path.split("/")[:-1]
    instance.file.delete(save=False)
    
    # Clean up empty directories
    
    # Check for empty folders in the path. Delete the first two.
    if len(path[-1]) == 32:
        # Path was (most likely) obscurified so we should look 2 levels down
        max_depth = 2
    else:
        max_depth = 1
    for depth in range(0, max_depth):
        delete_path = "/".join(path[:-depth] if depth > 0 else path)
        try:
            if len(os.listdir(os.path.join(django_settings.MEDIA_ROOT, delete_path))) == 0:
                os.rmdir(delete_path)
        except OSError:
            # Raised by os.listdir if directory is missing
            pass

signals.pre_delete.connect(on_revision_delete, AttachmentRevision)
