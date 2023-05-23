from django.test import TestCase
from rest_framework.test import APITestCase
# Create your tests here.
class UserTest(APITestCase):
    def user_tests(self):
        response = self.client('api/v1/user/profile/')
        print(response)