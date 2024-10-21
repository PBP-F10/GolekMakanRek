from django.urls import path
from homepage.views import *
# from .views import get_food
# from .views import get_restaurant

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('search/<str:type>/', search, name='search'),
    path('toggle_like/', toggle_like, name='toggle_like'),
    path('get_food/', get_food, name='get_food'),
    path('get_restaurant/', get_restaurant, name='get_restaurant'),
    path('get_likes/', get_likes, name='get_likes'),
]