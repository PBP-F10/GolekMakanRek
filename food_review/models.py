from django.db import models
from django.contrib.auth.models import User
from main.models import *

class FoodRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deskripsi_food = models.ForeignKey(Food, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    waktu_comment = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1, rating__lte=5), name="rating")
        ] 