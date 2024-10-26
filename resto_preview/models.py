from django.db import models
from django.contrib.auth.models import User

class show_resto(models.Model):
    id = models.AutoField(primary_key=True)    
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    deskripsi = models.TextField()
    random_products = models.JSONField(default=list, blank=True)

class Rating(models.Model):
    restaurant = models.ForeignKey(show_resto, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField() 

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(show_resto, on_delete=models.CASCADE)  
