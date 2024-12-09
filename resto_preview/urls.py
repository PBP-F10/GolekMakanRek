from django.urls import path
from . import views

app_name = 'resto_preview'

urlpatterns = [
    path('', views.restaurant_preview, name='restaurant_preview'),
    path('<uuid:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('<uuid:restaurant_id>/submit-rating/', views.submit_rating, name='submit_rating'),
    path('follow/<uuid:restaurant_id>/', views.follow_restaurant, name='follow_restaurant'), 
    path('unfollow/<uuid:restaurant_id>/', views.unfollow_restaurant, name='unfollow_restaurant'), 
]

