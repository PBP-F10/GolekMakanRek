from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from main.models import Restaurant, Food
from .models import FoodRating

class FoodReview(TestCase):
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

    def test_food_preview(self):
        response = Client().get('/food_review/')
        self.assertEqual(response.status_code, 200)
    
    def test_restaurant_detail(self):
        client = Client()
        response = client.get(f'/food_review/{Restaurant.objects.first().id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_add_rating(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        response = client.post(f'/food_review/add-rating/{Food.objects.first().id}/', {'comment': 'Test', 'score': 5})
        self.assertEqual(response.status_code, 200)
    
    def test_edit_rating(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        client.post(f'/food_review/add-rating/{Food.objects.first().id}/', {'comment': 'Test', 'score': 5})
        response = client.post(f'/food_review/edit-rating/{FoodRating.objects.first().id}/', {'comment': 'Test', 'score': 3})
        self.assertEqual(response.status_code, 200)
    
    def test_delete_rating(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        client.post(f'/food_review/add-rating/{Food.objects.first().id}/', {'comment': 'Test', 'score': 5})
        response = client.post(f'/food_review/delete-rating/{FoodRating.objects.first().id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_user_ratings(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        response = client.get(f'/food_review/get-user-rating/{Food.objects.first().id}/')
        self.assertEqual(response.status_code, 200)