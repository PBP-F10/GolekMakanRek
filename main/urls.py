from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('food_json/', views.food_json, name='food'),
    path('restaurant_json/', views.restaurant_json, name='restaurant'),
]