from django.test import TestCase
from wiki.core.utils import object_to_json_response


class TestUtils(TestCase):

    def test_object_to_json(self):
        """
        Simple test, the actual serialization happens in json.dumps and we
        don't wanna test this core module in depth.
        """
        obj = []
        response = object_to_json_response(obj)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")
