from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import *

# Create your tests here.
class RestoPreview(TestCase):
    def setUp(self):
        self.user1 = User(username="tes")
        self.user1.set_password("testpass123")
        self.user1.save()

        self.resto = show_resto.objects.create(
            nama = 'Test',
            kategori = 'Test',
            deskripsi = 'Test',
        )
        self.resto.save()

    def test_restaurant_preview(self):
        response = Client().get('/restaurant/')
        self.assertEqual(response.status_code, 200)
    
    def test_restaurant_detail(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        response = client.get(f'/restaurant/{show_resto.objects.first().id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_restaurant_rating(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        client.post(f'/restaurant/restaurants/{show_resto.objects.first().id}/submit-rating/', {'score': 5})
        response = client.post(f'/restaurant/{show_resto.objects.first().id}/submit-rating/', {'score': 3})
        self.assertEqual(response.status_code, 200)
    
    def test_restaurant_follow(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        response = client.post(f'/restaurant/follow/{show_resto.objects.first().id}/')
        self.assertEqual(Follow.objects.all().count(), 1)