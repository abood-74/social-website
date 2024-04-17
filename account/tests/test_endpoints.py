from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
import pytest
from account.models import CustomUser
from actions.models import Action




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
        self.assertEqual(len(Action.objects.all()), 1)
    
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
        
        

class UserListViewTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_user_list_view(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword', email = 'a.ex.com')
        self.client.force_authenticate(user=user)
        
        response = self.client.get(reverse("account:users"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['username'] == 'testuser'
        assert response.data[0]['email'] == 'a.ex.com'

class UserDetailViewTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_user_detail_view(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword', email = 'a.ex.com')
        self.client.force_authenticate(user=user)
        
        response = self.client.get(reverse("account:user-detail"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
        assert response.data['email'] == 'a.ex.com'
        assert response.data['first_name'] == ''
        assert response.data['following'] == []
        
        

class FollowUserViewTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_follow_user_with_valid_data(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword', email = 'a.e.com')
        user2 = CustomUser.objects.create_user(username='testuser2', password='testpassword', email = 'a.ex.com')
        self.client.force_authenticate(user=user)
        
        data = {
            'id': user2.id,
            'action': 'follow'
        }
        
        response = self.client.post(reverse("account:follow"), data)
        
        assert response.status_code == status.HTTP_200_OK
        assert user.following.count() == 1
        assert user.following.first().username == 'testuser2'
        assert Action.objects.count() == 1
        
        
        
    def test_follow_user_with_invalid_data(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword', email = 'a.e.com')
        user2 = CustomUser.objects.create_user(username='testuser2', password='testpassword', email = 'a.ex.com')
        
        self.client.force_authenticate(user=user)

        data = {
            'id': user2.id,
            'action': 'unfollow'
        }
        
        response = self.client.post(reverse("account:follow"), data)
        
        assert response.status_code == status.HTTP_200_OK
        assert user.following.count() == 0
        assert Action.objects.count() == 0

        
    def test_follow_user_with_invalid_action(self):
        user2 = CustomUser.objects.create_user(username='testuser2', password='testpassword', email = 'a.ex.com')
        
        self.client.force_authenticate(user=user2)

        data = {
            'id': user2.id,
            'action': 'invalid'
        }
        
        response = self.client.post(reverse("account:follow"), data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'message' in response.data
        

class UserDashboardViewTests(APITestCase):
        
        def setUp(self):
            self.client = APIClient()
        
        def test_user_dashboard_view(self):
            user = CustomUser.objects.create_user(username='testuser', password='testpassword', email = 'a.e.com')
            user2 = CustomUser.objects.create_user(username='testuser2', password='testpassword', email = 'a.ex.com')
            user.following.add(user2)
            user2.following.add(user)
            Action.objects.create(user=user2, verb='follow', target=user)
            
            
            self.client.force_authenticate(user=user)
            
            response = self.client.get(reverse("account:dashboard"))
            
            assert response.status_code == status.HTTP_200_OK
            assert response.data[0]['user'] == user2.id
            assert response.data[0]['verb'] == 'follow'
            
           
        


