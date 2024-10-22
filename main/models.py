from django.db import models
import uuid

# Create your models here.
class Food(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    harga = models.IntegerField()
    diskon = models.IntegerField()
    deskripsi = models.TextField()
    restoran = models.ForeignKey('Restaurant', on_delete=models.CASCADE)

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    deskripsi = models.TextField()