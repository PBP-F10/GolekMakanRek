from django.urls import path
from .views import show_post, add_post, like_post, comment_post, report_post, search_restaurants, list_restaurants


app_name = 'forum'

urlpatterns = [
    path('', show_post, name='show_post'),
    path('add_post/', add_post, name='add_post'),
    path('like_post/', like_post, name='like_post'), # New URL for the like request  
    path('comment_post/', comment_post, name='comment_post'), # New URL for the like request   
    path('report_post/', report_post, name='report_post'), # New URL for the like request   
    path('search_restaurants/', search_restaurants, name='search_restaurants'),
    path('list_restaurants/', list_restaurants, name='list_restaurants'),



]