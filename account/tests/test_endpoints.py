from account.models import CustomUser
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
import pytest



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
        

    def test_login_with_invalid_credentials(self):
        data = {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        }
        
        response = self.client.post(reverse("account:login"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
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

class RegisterViewTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_register_with_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'a@er.com',
            'password': 'testpassword',
            'password2':'testpassword'
            
        }
        
        response = self.client.post(reverse("account:register"), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_register_with_invalid_data(self):
        
        data = {
            'username': '',
            'password': ''
        }
        
        response = self.client.post(reverse("account:register"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

class PasswordChangeViewTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_password_change_with_valid_data(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword', email = 'abood@ex.com')
        self.client.force_authenticate(user=user)
        
        data = {
            'password': 'newpassword1545'
        }
        
        response = self.client.post(reverse("account:password-change"), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password changed successfully')
    
    def test_password_change_with_invalid_data(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword', email = 'abood@ex.com')
        self.client.force_authenticate(user=user)
        
        data = {
            'password': 'short'
        }
        response = self.client.post(reverse("account:password-change"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EditUserViewTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_edit_user_with_valid_data(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword', email = 'abood@ex.com')
        self.client.force_authenticate(user=user)
        put_data = {
            'username': 'testuser',
            'email': 'a@er.com',
            'first_name': 'test'
            
        }
        
        patch_data = {
            'username': 'testuser',
        }
        
        put_response = self.client.put(reverse("account:edit"), put_data)
        patch_response = self.client.patch(reverse("account:edit"), patch_data)
        
        self.assertEqual(put_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(patch_response.status_code, status.HTTP_201_CREATED)
        


