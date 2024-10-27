from django.urls import path
from . import views

app_name = 'resto_preview'

urlpatterns = [
    path('', views.restaurant_preview, name='restaurant_preview'),
    path('<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('<int:restaurant_id>/submit-rating/', views.submit_rating, name='submit_rating'), 
]
