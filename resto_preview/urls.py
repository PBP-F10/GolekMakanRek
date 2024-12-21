from django.urls import path
from . import views

app_name = 'resto_preview'

urlpatterns = [
    path('', views.restaurant_preview, name='restaurant_preview'),
    path('<uuid:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('<uuid:restaurant_id>/submit-rating/', views.submit_rating, name='submit_rating'),
    path('follow/<uuid:restaurant_id>/', views.follow_restaurant, name='follow_restaurant'), 
    path('unfollow/<uuid:restaurant_id>/', views.unfollow_restaurant, name='unfollow_restaurant'), 

    path('restorating_json/', views.restorating_json, name='resto_rating'),
    path('get-restaurant-rating/<uuid:restaurant_id>/', views.get_restaurant_rating, name='get_restaurant_rating'),
    path('get-user-rating/<uuid:restaurant_id>/', views.get_user_rating, name='get_user_rating'),

    path('restofollow_json/', views.restofollow_json, name='resto_follow'),
    path('status/', views.get_follow_status, name='get_follow_status'),
]

