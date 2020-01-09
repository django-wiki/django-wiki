"""Here is a very basic handling of accounts.
If you have your own account handling, don't worry,
just switch off account handling in
settings.WIKI_ACCOUNT_HANDLING = False

and remember to set
settings.WIKI_SIGNUP_URL = '/your/signup/url'
SETTINGS.LOGIN_URL
SETTINGS.LOGOUT_URL
"""

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import (
    get_user_model,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, FormView, UpdateView, View
from wiki import forms
from wiki.conf import settings

User = get_user_model()


class Signup(CreateView):
    model = User
    form_class = forms.UserCreationForm
    template_name = "wiki/accounts/signup.html"

    def dispatch(self, request, *args, **kwargs):
        # Let logged in super users continue
        if not request.user.is_anonymous and not request.user.is_superuser:
            return redirect("wiki:root")
        # If account handling is disabled, don't go here
        if not settings.ACCOUNT_HANDLING:
            return redirect(settings.SIGNUP_URL)
        # Allow superusers to use signup page...
        if not request.user.is_superuser and not settings.ACCOUNT_SIGNUP_ALLOWED:
            c = {"error_msg": _("Account signup is only allowed for administrators.")}
            return render(request, "wiki/error.html", context=c)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["honeypot_class"] = context["form"].honeypot_class
        context["honeypot_jsfunction"] = context["form"].honeypot_jsfunction
        return context

    def get_success_url(self, *args):
        messages.success(
            self.request, _("You are now signed up... and now you can sign in!")
        )
        return reverse("wiki:login")


class Logout(View):
    def dispatch(self, request, *args, **kwargs):
        if not settings.ACCOUNT_HANDLING:
            return redirect(settings.LOGOUT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        messages.info(request, _("You are no longer logged in. Bye bye!"))
        return redirect("wiki:root")


class Login(FormView):

    form_class = AuthenticationForm
    template_name = "wiki/accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect("wiki:root")
        if not settings.ACCOUNT_HANDLING:
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        self.request.session.set_test_cookie()
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        self.referer = request.session.get("login_referer", "")
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.referer = request.META.get("HTTP_REFERER", "")
        request.session["login_referer"] = self.referer
        return super().get(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        auth_login(self.request, form.get_user())
        messages.info(self.request, _("You are now logged in! Have fun!"))
        if self.request.GET.get("next", None):
            return redirect(self.request.GET["next"])
        if django_settings.LOGIN_REDIRECT_URL:
            return redirect(django_settings.LOGIN_REDIRECT_URL)
        else:
            if not self.referer:
                return redirect("wiki:root")
            return redirect(self.referer)


class Update(UpdateView):
    model = User
    form_class = forms.UserUpdateForm
    template_name = "wiki/accounts/account_settings.html"

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        """
        Save the initial referer
        """
        self.referer = request.META.get("HTTP_REFERER", "")
        request.session["login_referer"] = self.referer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.referer = request.session.get("login_referer", "")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        pw = form.cleaned_data["password1"]
        if pw != "":
            self.object.set_password(pw)
        self.object.save()

        messages.info(self.request, _("Account info saved!"))

        # Redirect after saving
        if self.referer:
            return redirect(self.referer)
        if django_settings.LOGIN_REDIRECT_URL:
            return redirect(django_settings.LOGIN_REDIRECT_URL)
        return redirect("wiki:root")
