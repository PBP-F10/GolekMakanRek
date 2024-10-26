from django.db import models
from django.contrib.auth.models import User
from main.models import Food

# Create your models here.
class Likes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)