import copy

from django.conf import settings
from django.core.checks import Error, registry
from django.test import TestCase
from wiki.checks import OBSOLETE_INSTALLED_APPS, REQUIRED_CONTEXT_PROCESSORS, REQUIRED_INSTALLED_APPS, Tags


def _remove(settings, arg):
    return [setting for setting in settings if not setting.startswith(arg)]


class CheckTests(TestCase):
    def test_required_installed_apps(self):
        for app in REQUIRED_INSTALLED_APPS:
            with self.settings(INSTALLED_APPS=_remove(settings.INSTALLED_APPS, app[0])):
                errors = registry.run_checks(tags=[Tags.required_installed_apps])
                expected_errors = [
                    Error(
                        'needs %s in INSTALLED_APPS' % app[1],
                        id='wiki.%s' % app[2],
                    )
                ]
                self.assertEqual(errors, expected_errors)

    def test_required_context_processors(self):
        for context_processor in REQUIRED_CONTEXT_PROCESSORS:
            TEMPLATES = copy.deepcopy(settings.TEMPLATES)
            TEMPLATES[0]['OPTIONS']['context_processors'] = [
                cp
                for cp in TEMPLATES[0]['OPTIONS']['context_processors']
                if cp != context_processor[0]
            ]
            with self.settings(TEMPLATES=TEMPLATES):
                errors = registry.run_checks(tags=[Tags.context_processors])
                expected_errors = [
                    Error(
                        "needs %s in TEMPLATE['OPTIONS']['context_processors']" % context_processor[0],
                        id='wiki.%s' % context_processor[1],
                    )
                ]
                self.assertEqual(errors, expected_errors)
