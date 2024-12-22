from django.urls import path
from .views import show_post, add_post, like_post, comment_post, report_post, search_restaurants
from .views import post_json, comment_json, like_json, report_json
from . import views

app_name = 'forum'

urlpatterns = [
    path('', show_post, name='show_post'),
    path('add_post/', add_post, name='add_post'),
    path('like_post/', like_post, name='like_post'), # New URL for the like request  
    path('comment_post/', comment_post, name='comment_post'), # New URL for the like request   
    path('report_post/', report_post, name='report_post'), # New URL for the like request   
    path('search_restaurants/', search_restaurants, name='search_restaurants'),
    path('post_json/', post_json, name='post_json'),
    path('like_json/', like_json, name='like_json'),
    path('comment_json/', comment_json, name='comment_json'),
    path('report_json/', report_json, name='report_json'),
    path('create_post_flutter/', views.create_post_flutter, name='create_post_flutter'),
    path('like_post_flutter/', views.like_post_flutter, name='like_post_flutter'),
    path('comment_post_flutter/', views.comment_post_flutter, name='comment_post_flutter'),
    path('report_post_flutter/', views.report_post_flutter, name='report_post_flutter'),
    path('get_all_users/', views.get_all_users, name='get_all_users'),
    path('edit_comment_flutter/', views.edit_comment_flutter, name='edit_comment_flutter'),
    path('delete_post_flutter/', views.delete_post_flutter, name='delete_post_flutter'),
    path('restaurant_json/', views.restaurant_json, name='restaurant_json'),
    path('like_post_flutter/', views.like_post_flutter, name='like_post_flutter'),
]