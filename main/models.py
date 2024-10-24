from django.db import models

# Create your models here.
class Food(models.Model):
    id = models.AutoField(primary_key=True)    
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    harga = models.IntegerField()
    diskon = models.IntegerField()
    deskripsi = models.TextField()
    restoran = models.ForeignKey('Restaurant', on_delete=models.CASCADE)

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)    
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    deskripsi = models.TextField()
    random_products = models.JSONField(default=list, blank=True)
    