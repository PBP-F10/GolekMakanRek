from django.db import models
from django.contrib.auth.models import User
import uuid
# from .models import Food
# from .models import Restaurant

# Create your models here.
class Food(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.IntegerField()
    description = models.TextField()
    
    @property
    def discounted_price(self):
        return self.price - self.discount
    
    @property
    def discount_percent(self):
        return round((self.discount / self.price) * 100)
    
    @property
    def is_discounted(self):
        return self.discount > 0

class Restaurant(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()

class Likes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)