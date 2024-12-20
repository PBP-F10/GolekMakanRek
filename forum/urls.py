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

]