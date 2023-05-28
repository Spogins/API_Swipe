from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class ComplexTests(APITestCase):
    def test_list_complex(self):
        url = 'api/v1/residential_complex'
        response = self.client.get(url, format='json')
        print(response)
