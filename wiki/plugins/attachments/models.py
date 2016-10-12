# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os.path

from django.conf import settings as django_settings
from django.db import models
from django.db.models import signals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from six.moves import map, range
from wiki import managers
from wiki.decorators import disable_signal_for_loaddata
from wiki.models.article import BaseRevisionMixin
from wiki.models.pluginbase import ReusablePlugin

from . import settings


class IllegalFileExtension(Exception):

    """File extension on upload is not allowed"""
    pass


@python_2_unicode_compatible
class Attachment(ReusablePlugin):

    objects = managers.ArticleFkManager()

    current_revision = models.OneToOneField(
        'AttachmentRevision', verbose_name=_('current revision'),
        blank=True, null=True, related_name='current_set',
        help_text=_(
            'The revision of this attachment currently in use (on all articles using the attachment)'),)

    original_filename = models.CharField(
        max_length=256,
        verbose_name=_('original filename'),
        blank=True,
        null=True)

    def can_write(self, user):
        if not settings.ANONYMOUS and (not user or user.is_anonymous()):
            return False
        return ReusablePlugin.can_write(self, user)

    def can_delete(self, user):
        return self.can_write(user)

    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')
        # Matches label of upcoming 0.1 release
        db_table = 'wiki_attachments_attachment'

    def __str__(self):
        from wiki.models import Article
        try:
            return "%s: %s" % (
                self.article.current_revision.title, self.original_filename)
        except Article.DoesNotExist:
            return "Attachment for non-existing article"


def extension_allowed(filename):
    try:
        extension = filename.split(".")[-1]
    except IndexError:
        # No extension
        raise IllegalFileExtension(
            ugettext("No file extension found in filename. That's not okay!"))
    if not extension.lower() in map(
            lambda x: x.lower(),
            settings.FILE_EXTENSIONS):
        raise IllegalFileExtension(
            ugettext(
                "The following filename is illegal: {filename:s}. Extension "
                "has to be one of {extensions:s}"
            ).format(
                filename=filename,
                extensions=", ".join(settings.FILE_EXTENSIONS)
            )
        )

    return extension


def upload_path(instance, filename):
    from os import path

    extension = extension_allowed(filename)

    # Has to match original extension filename
    if instance.id and instance.attachment and instance.attachment.original_filename:
        original_extension = instance.attachment.original_filename.split(
            ".")[-1]
        if not extension.lower() == original_extension:
            raise IllegalFileExtension(
                "File extension has to be '%s', not '%s'." %
                (original_extension, extension.lower()))
    elif instance.attachment:
        instance.attachment.original_filename = filename

    upload_path = settings.UPLOAD_PATH
    upload_path = upload_path.replace(
        '%aid', str(
            instance.attachment.article.id))
    if settings.UPLOAD_PATH_OBSCURIFY:
        import random
        import hashlib
        m = hashlib.md5(
            str(random.randint(0, 100000000000000)).encode('ascii'))
        upload_path = path.join(upload_path, m.hexdigest())

    if settings.APPEND_EXTENSION:
        filename += '.upload'
    return path.join(upload_path, filename)


@python_2_unicode_compatible
class AttachmentRevision(BaseRevisionMixin, models.Model):

    attachment = models.ForeignKey('Attachment')

    file = models.FileField(upload_to=upload_path,  # @ReservedAssignment
                            max_length=255,
                            verbose_name=_('file'),
                            storage=settings.STORAGE_BACKEND)

    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('attachment revision')
        verbose_name_plural = _('attachment revisions')
        ordering = ('created',)
        get_latest_by = 'revision_number'
        # Matches label of upcoming 0.1 release
        db_table = 'wiki_attachments_attachmentrevision'

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

    def __str__(self):
        return "%s: %s (r%d)" % (self.attachment.article.current_revision.title,
                                 self.attachment.original_filename,
                                 self.revision_number)

@disable_signal_for_loaddata
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
            if len(
                os.listdir(
                    os.path.join(
                        django_settings.MEDIA_ROOT,
                        delete_path))) == 0:
                os.rmdir(delete_path)
        except OSError:
            # Raised by os.listdir if directory is missing
            pass


@disable_signal_for_loaddata
def on_attachment_revision_pre_save(**kwargs):
    instance = kwargs['instance']
    if kwargs.get('created', False):
        update_previous_revision = (
            not instance.previous_revision and
            instance.attachment and
            instance.attachment.current_revision and
            instance.attachment.current_revision != instance
        )
        if update_previous_revision:
            instance.previous_revision = instance.attachment.current_revision

    if not instance.revision_number:
        try:
            previous_revision = instance.attachment.attachmentrevision_set.latest()
            instance.revision_number = previous_revision.revision_number + 1
        # NB! The above should not raise the below exception, but somehow
        # it does.
        except (AttachmentRevision.DoesNotExist, Attachment.DoesNotExist):
            instance.revision_number = 1


@disable_signal_for_loaddata
def on_attachment_revision_post_save(**kwargs):
    instance = kwargs['instance']
    if not instance.attachment.current_revision:
        # If I'm saved from Django admin, then article.current_revision is
        # me!
        instance.attachment.current_revision = instance
        instance.attachment.save()


signals.pre_delete.connect(on_revision_delete, AttachmentRevision)
signals.pre_save.connect(on_attachment_revision_pre_save, AttachmentRevision)
signals.post_save.connect(on_attachment_revision_post_save, AttachmentRevision)
