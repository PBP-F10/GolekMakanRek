from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from main.models import Food, Restaurant
import json

# Create your tests here.
class Homepage(TestCase):
    def setUp(self):
        self.user1 = User(username="Test")
        self.user1.set_password("testpass123")
        self.user1.save()

    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_index_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'index.html')

    def test_nonexistent_page(self):
        response = Client().get('/skibidi/')
        self.assertEqual(response.status_code, 404)
    
    def test_all_food(self):
        response = Client().get('/get_food/')
        self.assertEqual(response.status_code, 200)

    def test_search_food(self):
        response = Client().get('/search/food/?nama=Test&min_harga=0&max_harga=1000000')
        self.assertEqual(response.status_code, 200)

    def test_food_liked(self):
        client = Client()
        client.login(username='Test', password='testpass123')
        response = client.get('/search/food/?like_filter=1')
        self.assertEqual(response.status_code, 200)

    def test_all_restaurant(self):
        response = Client().get('/get_restaurant/')
        self.assertEqual(response.status_code, 200)

    def test_search_restaurant(self):
        response = Client().get('/search/restaurant/?nama=Test')
        self.assertEqual(response.status_code, 200)
    
    def test_get_user_likes(self):
        client = Client()
        client.login(username='Test', password='testpass123')
        response = client.get('/get_user_likes/')
        self.assertEqual(response.status_code, 200)
    
    def test_add_likes(self):
        resto = Restaurant.objects.create(
            nama = 'Test',
            kategori = 'Test',
            deskripsi = 'Test',
        )
        resto.save()
        food = Food.objects.create(
            nama = 'Test',
            kategori = 'Test',
            harga = 10000,
            diskon = 0,
            deskripsi = 'Test',
            restoran = resto,
        )
        food.save()
        client = Client()
        client.login(username='Test', password='testpass123')
        response = client.post('/toggle_like/', {'food_id': food.id, 'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
    
    def test_register(self):
        response = Client().post('/register/', {'username': 'Test2', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        response = Client().post('/login/', {'username': 'Test', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 302)
    
    def test_logout(self):
        client = Client()
        client.login(username='Test', password='testpass123')
        response = client.get('/logout/')
        self.assertEqual(response.status_code, 302)