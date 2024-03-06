from account.models import CustomUser
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


class LoginViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_with_valid_credentials(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse("account:login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You have been logged in')

    def test_login_with_invalid_credentials(self):
        data = {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        }
        response = self.client.post(reverse("account:login"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid credentials')

    def test_login_with_invalid_data(self):
        data = {
            'username': '',
            'password': ''
        }
        
        response = self.client.post(reverse("account:login"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
