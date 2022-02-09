from django.conf import settings as django_settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import resolve_url
from wiki.conf import settings as wiki_settings
from wiki.models import reverse

from ..base import ArticleWebTestUtils
from ..base import DjangoClientTestBase
from ..base import RequireRootArticleMixin
from ..base import SUPERUSER1_PASSWORD
from ..base import SUPERUSER1_USERNAME
from ..base import TestBase
from ..base import wiki_override_settings
from ..testdata.models import CustomUser


SIGNUP_TEST_USERNAME = "wiki"
SIGNUP_TEST_PASSWORD = "wiki1234567"


class AccountUpdateTest(
    RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase
):
    def test_password_change(self):
        """
        Test that we can make a successful password change via the update form
        """
        # Check out that it works as expected, notice that there is no referrer
        # on this GET request.
        self.client.get(
            resolve_url(
                "wiki:profile_update",
            )
        )

        # Now check that we don't succeed with unmatching passwords
        example_data = {
            "password1": "abcdef",
            "password2": "abcdef123",
            "email": self.superuser1.email,
        }

        # save a new revision
        response = self.client.post(resolve_url("wiki:profile_update"), example_data)
        self.assertContains(
            response, "Passwords don", status_code=200
        )  # Django 2/3 output different escaped versions of single quote in don't

        # Now check that we don't succeed with unmatching passwords
        example_data = {
            "password1": "abcdef",
            "password2": "abcdef",
            "email": self.superuser1.email,
        }

        # save a new revision
        response = self.client.post(resolve_url("wiki:profile_update"), example_data)

        # Need to force str() because of:
        # TypeError: coercing to Unicode: need string or buffer, __proxy__
        # found
        self.assertRedirects(response, str(django_settings.LOGIN_REDIRECT_URL))

        self.assertEqual(
            self.superuser1,
            authenticate(
                username=self.superuser1.username, password=example_data["password1"]
            ),
        )


class UpdateProfileViewTest(
    RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase
):
    def test_update_profile(self):
        self.client.post(
            resolve_url("wiki:profile_update"),
            {"email": "test@test.com", "password1": "newPass", "password2": "newPass"},
            follow=True,
        )

        test_auth = authenticate(username="admin", password="newPass")

        self.assertIsNotNone(test_auth)
        self.assertEqual(test_auth.email, "test@test.com")


@wiki_override_settings(ACCOUNT_HANDLING=True)
class LogoutViewTests(RequireRootArticleMixin, DjangoClientTestBase):
    def test_logout_account_handling(self):
        self.client.get(wiki_settings.LOGOUT_URL)
        user = auth.get_user(self.client)
        self.assertIs(auth.get_user(self.client).is_authenticated, False)
        self.assertIsInstance(user, AnonymousUser)


@wiki_override_settings(ACCOUNT_HANDLING=True)
class LoginTestViews(RequireRootArticleMixin, TestBase):
    def test_already_signed_in(self):
        self.client.force_login(self.superuser1)
        response = self.client.get(wiki_settings.LOGIN_URL)
        self.assertRedirects(response, reverse("wiki:root"))

    def test_log_in(self):
        self.client.post(
            wiki_settings.LOGIN_URL,
            {"username": SUPERUSER1_USERNAME, "password": SUPERUSER1_PASSWORD},
        )
        self.assertIs(self.superuser1.is_authenticated, True)
        self.assertEqual(auth.get_user(self.client), self.superuser1)


class SignupViewTests(RequireRootArticleMixin, TestBase):
    @wiki_override_settings(ACCOUNT_HANDLING=True, ACCOUNT_SIGNUP_ALLOWED=True)
    def test_signup(self):
        response = self.client.post(
            wiki_settings.SIGNUP_URL,
            data={
                "password1": SIGNUP_TEST_PASSWORD,
                "password2": SIGNUP_TEST_PASSWORD,
                "username": SIGNUP_TEST_USERNAME,
                "email": "wiki@wiki.com",
            },
        )
        self.assertIs(CustomUser.objects.filter(email="wiki@wiki.com").exists(), True)
        self.assertRedirects(response, reverse("wiki:login"))

        # Test that signing up the same user again gives a validation error
        # Regression test: https://github.com/django-wiki/django-wiki/issues/1152
        response = self.client.post(
            wiki_settings.SIGNUP_URL,
            data={
                "password1": SIGNUP_TEST_PASSWORD,
                "password2": SIGNUP_TEST_PASSWORD,
                "username": SIGNUP_TEST_USERNAME,
                "email": "wiki@wiki.com",
            },
        )
        self.assertIs(response.status_code, 200)
        self.assertContains(response, "username already exists")
