from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User

class UserTestCase(APITestCase):
    def setUp(self):
        pass

    # 회원가입 test
    def test_register_user(self):
        url = '/user/register/'
        data = {'phone_number' : '010-1234-5678', 'password' : 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)