from django.shortcuts import resolve_url
from django_nyt.models import Settings
from tests.base import (
    ArticleWebTestUtils,
    DjangoClientTestBase,
    RequireRootArticleMixin,
)


class NotificationSettingsTests(
    RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase
):
    def setUp(self):
        super().setUp()

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(resolve_url("wiki:notification_settings"))
        self.assertEqual(response.status_code, 302)

    def test_when_logged_in(self):
        response = self.client.get(resolve_url("wiki:notification_settings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wiki/plugins/notifications/settings.html")

    def test_change_settings(self):
        self.settings, __ = Settings.objects.get_or_create(
            user=self.superuser1, is_default=True
        )

        url = resolve_url("wiki:notification_settings")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {"csrf_token": response.context["csrf_token"]}

        # management form information, needed because of the formset
        management_form = response.context["form"].management_form

        for i in "TOTAL_FORMS", "INITIAL_FORMS", "MIN_NUM_FORMS", "MAX_NUM_FORMS":
            data["%s-%s" % (management_form.prefix, i)] = management_form[i].value()

        for i in range(response.context["form"].total_form_count()):
            # get form index 'i'
            current_form = response.context["form"].forms[i]

            # retrieve all the fields
            for field_name in current_form.fields:
                value = current_form[field_name].value()
                data["%s-%s" % (current_form.prefix, field_name)] = (
                    value if value is not None else ""
                )

        data["form-TOTAL_FORMS"] = 1
        data["form-0-email"] = 2
        data["form-0-interval"] = 0
        # post the request without any change

        response = self.client.post(url, data, follow=True)

        self.assertEqual(len(response.context.get("messages")), 1)

        message = response.context.get("messages")._loaded_messages[0]
        self.assertIn(
            message.message, "You will receive notifications instantly for 0 articles"
        )

        # Ensure we didn't create redundant Settings objects
        assert self.superuser1.nyt_settings.all().count() == 1
