from django.urls import path
from . import views

app_name = 'resto_preview'

urlpatterns = [
    path('restaurants/', views.restaurant_preview, name='restaurant_preview'),
    path('restaurants/<int:id>/', views.restaurant_detail, name='restaurant_detail'),
]
