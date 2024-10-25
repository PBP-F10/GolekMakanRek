from django.db import models
from django.contrib.auth.models import User
from main.models import Food

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Food, on_delete=models.CASCADE)