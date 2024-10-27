from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from main.models import Restaurant

# Create your tests here.
class UserProfile(TestCase):
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

    def test_user_profile(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        response = client.get('/userprofile/userprofile')
        self.assertEqual(response.status_code, 200)
    
    def test_user_profile_get(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        response = client.get(f'/userprofile/userprofile/get')
        self.assertEqual(response.status_code, 200)
    
    def test_user_profile_edit(self):
        client = Client()
        client.login(username='tes', password='testpass123')
        response = client.post(f'/userprofile/userprofiel/update', {'first_name': 'Test', 'last_name': 'Test', 'email': 'test@test.com', 'username': 'tes', 'description': 'Test'})
        self.assertEqual(response.status_code, 200)
