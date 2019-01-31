from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    some_field = models.IntegerField(default=0)


class CustomGroup(models.Model):
    pass


# user with invalid renamed identifier, and no email field
class VeryCustomUser(AbstractBaseUser):
    identifier = models.IntegerField()
    USERNAME_FIELD = 'identifier'
