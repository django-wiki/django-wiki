from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    some_field = models.IntegerField(default=0)

    custom_groups = models.ManyToManyField(
        "CustomGroup",
        verbose_name="groups",
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )


class CustomGroup(models.Model):
    pass


# user with invalid renamed identifier, and no email field
class VeryCustomUser(AbstractBaseUser):
    identifier = models.IntegerField()
    USERNAME_FIELD = "identifier"
