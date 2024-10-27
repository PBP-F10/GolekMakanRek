from django.db import models
from django.contrib.auth.models import User
from main.models import *

class FoodRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deskripsi_food = models.ForeignKey(Food, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating score between 1 and 5"
    )
    comment = models.TextField(blank=True, null=True)
    waktu_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s rating for {self.deskripsi_food.nama}"