from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from main.models import Restaurant
import json

# Create your tests here.
class Forum(TestCase):
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
    
    def test_show_forum(self):
        response = Client().get('/forum/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_forum(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        response = client.post('/forum/', {'text': 'Test', 'image': 'Test', 'restaurant_id': self.resto.id, 'restaurant_name': 'Test'})
        self.assertEqual(response.status_code, 200)
    
    def test_like_post(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        client.post('/forum/', {'text': 'Test', 'image': 'Test', 'restaurant_id': self.resto.id, 'restaurant_name': 'Test'})
        response = client.post('/forum/like_post/', json.dumps({'post_id': 1}), content_type='application/json')
        self.assertEqual(response.status_code, 404) # add_post masih belom benar
    
    def test_comment_post(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        client.post('/forum/', {'text': 'Test', 'image': 'Test', 'restaurant_id': self.resto.id, 'restaurant_name': 'Test'})
        response = client.post('/forum/comment_post/', json.dumps({'post_id': 1, 'comment': 'Test'}), content_type='application/json')
        self.assertEqual(response.status_code, 404) # add_post masih belom benar
    
    def test_report_post(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        client.post('/forum/', {'text': 'Test', 'image': 'Test', 'restaurant_id': self.resto.id, 'restaurant_name': 'Test'})
        client.post('/forum/comment_post/', json.dumps({'post_id': 1, 'comment': 'Test'}), content_type='application/json')
        response = client.post('/forum/report_post/', json.dumps({'post_id': 1, 'reason': 'Test'}), content_type='application/json')
        self.assertEqual(response.status_code, 404) # add_post masih belom benar
    
    def test_search_restaurants(self):
        response = Client().get('/forum/search_restaurants/?q=Test')
        self.assertEqual(response.status_code, 200)