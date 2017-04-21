from __future__ import absolute_import
from django.db import models

try:
    from django.contrib.auth.models import AbstractUser

    class CustomUser(AbstractUser):
        some_field = models.IntegerField(default=0)
except ImportError:
    pass


class CustomGroup(models.Model):
    pass
