from django.test import TestCase
from .models import Owner
# Create your tests here.


class OwnerTess(TestCase):


    def test_create_owner(self):
        owner = Owner.objects.get(id=1)
        expected_object_name = f'{owner.text}'
        self.assertEqual(expected_object_name, 'just a test')