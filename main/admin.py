from django.contrib import admin

# Register your models here.
# GolekMakanRek/main/admin.py

from django.contrib import admin
from .models import Food, Restaurant

admin.site.register(Food)
admin.site.register(Restaurant)
