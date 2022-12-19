from unittest import TestCase

from ..models import Owner
from ..serializers import OwnerSerializer


class OwnerSerializerTestCase(TestCase):
    def test_ok(self):
        owner_1 = Owner.objects.create(owner_name='Test1', owner_description='test1', link='test1', owner_status=1)
        owner_2 = Owner.objects.create(owner_name='Test2', owner_description='test2', link='test2', owner_status=0)
        data = OwnerSerializer([owner_1, owner_2], many=True).data
        expected_data = [
            {id: owner_1.id, 'owner_name': 'Test1', 'owner_description': 'test1', 'link': 'test1', 'owner_status': 1},
            {id: owner_2.id, 'owner_name': 'Test2', 'owner_description': 'test2', 'link': 'test2', 'owner_status': 0}]
        self.assertEqual(expected_data, data)
