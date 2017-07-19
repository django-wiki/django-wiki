from __future__ import absolute_import, print_function, unicode_literals


from django.conf import settings as django_settings
from django.contrib.auth import authenticate
from django.shortcuts import resolve_url

from ..base import (ArticleWebTestUtils, DjangoClientTestBase,
                    RequireRootArticleMixin)


class AccountUpdateTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_password_change(self):
        """
        Test that we can make a successful password change via the update form
        """
        c = self.c

        # Check out that it works as expected, notice that there is no referrer
        # on this GET request.
        c.get(
            resolve_url('wiki:profile_update',)
        )

        # Now check that we don't succeed with unmatching passwords
        example_data = {
            'password1': 'abcdef',
            'password2': 'abcdef123',
            'email': self.superuser1.email,
        }

        # save a new revision
        response = c.post(
            resolve_url('wiki:profile_update'),
            example_data
        )
        self.assertContains(response, "Passwords don&#39;t match", status_code=200)

        # Now check that we don't succeed with unmatching passwords
        example_data = {
            'password1': 'abcdef',
            'password2': 'abcdef',
            'email': self.superuser1.email,
        }

        # save a new revision
        response = c.post(
            resolve_url('wiki:profile_update'),
            example_data
        )

        # Need to force str() because of:
        # TypeError: coercing to Unicode: need string or buffer, __proxy__
        # found
        self.assertRedirects(response, str(django_settings.LOGIN_REDIRECT_URL))

        self.assertEqual(
            self.superuser1,
            authenticate(
                username=self.superuser1.username,
                password=example_data['password1']
            )
        )
