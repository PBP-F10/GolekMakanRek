from django.contrib import admin
from .models import *

class RatingComment(admin.ModelAdmin):
    list_display = ('id', 'user', 'deskripsi_food', 'score', 'comment', 'waktu_comment')

admin.site.register(FoodRating, RatingComment)