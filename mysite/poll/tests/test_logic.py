from django.test import TestCase
from ..logic import operations
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.mysite.settings")

class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(5, 13, '+')
        self.assertEqual(18, result)
