from django.contrib import admin
from .models import Likes
from main.models import Food, Restaurant

# Register your models here.
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'kategori', 'harga', 'diskon', 'deskripsi')

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'kategori', 'deskripsi')

class LikesAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'food_id')

admin.site.register(Food, FoodAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Likes, LikesAdmin)