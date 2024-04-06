from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
import pytest
from images.models import Image
from account.models import CustomUser
from actions.models import Action

@pytest.mark.django_db
class ImageCreateAPIViewTests(APITestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
    
    def test_create_image_with_valid_data(self):
        data = {
            'url': 'https://miro.medium.com/v2/resize:fit:828/format:webp/1*DsuteYpIwAq4frAeP_-OuA.png',
            'title': 'Google Logo',
            'slug': 'google-logo',
        }
        
        response = self.client.post(reverse("images:create"), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(Image.objects.get().title, 'Google Logo')
        self.assertEqual(Action.objects.count(), 1)   
    
    def test_create_image_with_invalid_url(self):
        data = {
            'url': 'https://miro.medium.com/v2/resize:fit:828/format:webp/1*DsuteYpIwAq4frAeP_-OuA.plg',
            'title': '',
            'slug': 'google-logo',
        }
        
        response = self.client.post(reverse("images:create"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Image.objects.count(), 0)
        self.assertIn('non_field_errors', response.data)
    
    def test_create_image_with_invalid_data(self):
        data = {
            'url': '',
            'title': '',
            'slug': '',
        }
        
        response = self.client.post(reverse("images:create"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Image.objects.count(), 0)
        self.assertIn('url', response.data)
        self.assertIn('slug', response.data)

@pytest.mark.django_db
class ImageDetailAPIViewTests(APITestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.image = Image.objects.create(url='https://img.freepik.com/free-photo/moon-light-shine-through-window-into-islamic-mosque-interior_1217-2597.jpg?w=1380&t=st=1712032626~exp=1712033226~hmac=df527b0cfb87586c5ae2b6202119c106c5faa0ebe149b7c0675b0f052735c067', title='Google Logo', slug='google-logo', user=user)
    
    def test_get_image_detail(self):
        response = self.client.get(reverse("images:detail", kwargs={'id': self.image.id}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Google Logo')
    
    def test_update_image_detail(self):
        data = {
            'title': 'Google Logo Updated'
        }
        
        response = self.client.put(reverse("images:detail", kwargs={'id': self.image.id}), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Image.objects.get().title, 'Google Logo Updated')
    
    def test_partial_update_image_detail(self):
        data = {
            'title': 'Google Logo Updated'
        }
        
        response = self.client.patch(reverse("images:detail", kwargs={'id': self.image.id}), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Image.objects.get().title, 'Google Logo Updated')
    
    def test_delete_image_detail(self):
        response = self.client.delete(reverse("images:detail", kwargs={'id': self.image.id}))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Image.objects.count(), 0)

