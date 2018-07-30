from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    some_field = models.IntegerField(default=0)


class CustomGroup(models.Model):
    pass
