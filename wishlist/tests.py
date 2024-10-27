from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from main.models import Restaurant, Food
from .models import Wishlist

# Create your tests here.
class WishlistUnitTest(TestCase):
    def setUp(self):
        self.user1 = User(username="tes")
        self.user1.set_password("testpass123")
        self.user1.save()

        self.resto = Restaurant.objects.create(
            nama = 'Test',
            kategori = 'Test',
            deskripsi = 'Test',
        )
        self.resto.save()
        self.food = Food.objects.create(
            nama = 'Test',
            kategori = 'Test',
            harga = 10000,
            diskon = 10,
            deskripsi = 'Test',
            restoran = self.resto,
        )
        self.food.save()

    def test_show_wishlist(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        response = client.get('/wishlist/')
        self.assertEqual(response.status_code, 200)