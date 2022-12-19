from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from ..models import Owner
from ..serializers import OwnerSerializer


class OwnerApiTestCase(APITestCase):
    def test_get(self):
        owner_1 = Owner.objects.create(owner_name='Test1', owner_description='test1', link='test1', owner_status=1)
        owner_2 = Owner.objects.create(owner_name='Test2', owner_description='test2', link='test2', owner_status=0)
        url = reverse('owner-list')

        response = self.client.get(url)
        serializer_data = OwnerSerializer([owner_1, owner_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

