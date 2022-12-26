from unittest import TestCase
import json
from collections import OrderedDict
from ..models import Owner
from ..serializers import OwnerSerializer


class OwnerSerializerTestCase(TestCase):
    def test_ok(self):
        owner_1 = Owner.objects.create(owner_name='Test1', owner_description='test1', link='test1', owner_status=1)
        owner_2 = Owner.objects.create(owner_name='Test2', owner_description='test2', link='test2', owner_status=0)
        data = OwnerSerializer([owner_1, owner_2], many=True).data
        data[0] = dict(data[0])
        data[1] = dict(data[1])

        expected_data = [
            {'id': owner_1.id, 'owner_name': 'Test1', 'owner_description': 'test1', 'link': 'test1', 'owner_status': 1, 'owner_img':None, 'created_by': None},
            {'id': owner_2.id, 'owner_name': 'Test2', 'owner_description': 'test2', 'link': 'test2', 'owner_status': 0, 'owner_img':None, 'created_by': None}]
        # for el in expected_data:
        #     print(type(el))
        print(data, expected_data)
        self.assertEqual(expected_data, data)
