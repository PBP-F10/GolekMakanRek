from django.contrib import admin
from .models import Likes
from main.models import Food, Restaurant

# Register your models here.
admin.site.register(Food)
admin.site.register(Restaurant)
admin.site.register(Likes)