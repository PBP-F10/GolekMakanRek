from django.urls import path
from homepage.views import *
# from .views import get_food
# from .views import get_restaurant

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('search/food/', search_food, name='search_food'),
    path('search/restaurant/', search_restaurant, name='search_restaurant'),
    path('toggle_like/', toggle_like, name='toggle_like'),
    path('toggle_like_json/', toggle_like_json, name='toggle_like_json'),
    path('get_food/', get_food, name='get_food'),
    path('get_restaurant/', get_restaurant, name='get_restaurant'),
    path('get_user_likes/', get_user_likes, name='get_user_likes'),
    path('get_food_likes/<uuid:food_id>', get_food_likes, name='get_food_likes'),
    path('get_search_options/', get_search_options, name='get_search_options'),
    # path('test/', set_test, name='test'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout')
]