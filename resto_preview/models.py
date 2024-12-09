from django.db import models
from django.contrib.auth.models import User
from main.models import *

class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField() 

    def total_ratings(self):
        return self.rating_set.count()

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  
