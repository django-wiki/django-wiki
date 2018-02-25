from django.contrib.auth.models import AbstractUser, GroupManager, PermissionManager
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CustomUser(AbstractUser):
    some_field = models.IntegerField(default=0)


class CustomPermission(models.Model):
    """Copy of Django's implementation"""
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, models.CASCADE)
    codename = models.CharField(max_length=100)
    objects = PermissionManager()

    class Meta:
        unique_together = (('content_type', 'codename'),)
        ordering = ('content_type__app_label', 'content_type__model',
                    'codename')

    def natural_key(self):
        return (self.codename,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']


class CustomGroup(models.Model):
    """
    Not trying to redefine the actual Django auth's group model, which seems
    to be a kind of permission specification in itself. We merely want to prove
    that we don't depend on the particular models.
    """

    name = models.CharField(max_length=80, unique=True)
    permissions = models.ManyToManyField(
        CustomPermission,
        blank=True,
    )
    objects = GroupManager()
