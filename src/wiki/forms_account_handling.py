import random
import string

import django.contrib.auth.models
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields import CharField
from django.db.models.fields import EmailField
from django.utils.translation import gettext_lazy as _
from wiki.conf import settings


def _get_field(model, field):
    try:
        return model._meta.get_field(field)
    except FieldDoesNotExist:
        return


User = get_user_model()


def check_user_field(user_model):
    return isinstance(_get_field(user_model, user_model.USERNAME_FIELD), CharField)


def check_email_field(user_model):
    return isinstance(
        _get_field(user_model, user_model.get_email_field_name()), EmailField
    )


# django parses the ModelForm (and Meta classes) on class creation, which fails with custom models without expected fields.
# We need to check this here, because if this module can't load then system checks can't run.
CustomUser = (
    User
    if (
        settings.ACCOUNT_HANDLING and check_user_field(User) and check_email_field(User)
    )
    else django.contrib.auth.models.User
)


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add honeypots
        self.honeypot_fieldnames = "address", "phone"
        self.honeypot_class = "".join(
            random.choice(string.ascii_uppercase + string.digits) for __ in range(10)
        )
        self.honeypot_jsfunction = "f" + "".join(
            random.choice(string.ascii_uppercase + string.digits) for __ in range(10)
        )

        for fieldname in self.honeypot_fieldnames:
            self.fields[fieldname] = forms.CharField(
                widget=forms.TextInput(attrs={"class": self.honeypot_class}),
                required=False,
            )

    def clean(self):
        super().clean()
        for fieldname in self.honeypot_fieldnames:
            if self.cleaned_data[fieldname]:
                raise forms.ValidationError(
                    "Thank you, non-human visitor. Please keep trying to fill in the form."
                )
        return self.cleaned_data

    class Meta:
        model = CustomUser
        fields = (CustomUser.USERNAME_FIELD, CustomUser.get_email_field_name())


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="New password", widget=forms.PasswordInput(), required=False
    )
    password2 = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput(), required=False
    )

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        return self.cleaned_data

    class Meta:
        model = CustomUser
        fields = [CustomUser.get_email_field_name()]
