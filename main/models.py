from django.db import models
import uuid
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    deskripsi = models.TextField()
    
    def __str__(self):
        return self.nama
    
    @property
    def average_rating(self):
        food_items = self.food_set.all()
        
        total_rating = 0
        total_count = 0
        
        for food in food_items:
            food_rating = food.average_rating
            if food_rating > 0:
                total_rating += food_rating
                total_count += 1
        
        return round(total_rating / total_count, 2) if total_count > 0 else 0

class Food(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    harga = models.IntegerField(validators=[MinValueValidator(0)])
    diskon = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Discount in percentage (0-100)"
    )
    deskripsi = models.TextField()
    restoran = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    
    @property
    def harga_setelah_diskon(self):
        return int(self.harga * (100 - self.diskon) / 100)
    
    @property
    def average_rating(self):
        avg_rating = self.foodrating_set.aggregate(Avg('score'))['score__avg']
        return round(avg_rating, 2) if avg_rating is not None else 0
    
    def __str__(self):
        return self.nama