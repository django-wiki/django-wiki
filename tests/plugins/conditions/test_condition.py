import markdown
from django.test import TestCase
from wiki.plugins.conditions.mdx.condition import ConditionExtension

class ConditionsTests(TestCase):
    def test_condition_user(self):
        """ Verifies that the [if user in ...] works as expected
        """
        md = markdown.Markdown(
            extensions=['extra', ConditionExtension()]
        )

        from django.contrib.auth import get_user_model
        User = get_user_model()

        md.user = User.objects.create_superuser('admin', 'nobody@example.com', 'secret' )

        text = (
            "start [if user in admin]admin[endif] [if user in jack]jack[endif] end\n"
        )
        expected_output = (
            '<p>start admin end</p>'
        )
        self.assertEqual(' '.join(md.convert(text).split()), expected_output)
