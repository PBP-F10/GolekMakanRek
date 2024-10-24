from django.urls import path
from .views import show_post, add_post, like_post, post_comment
app_name = 'forum'

urlpatterns = [
    path('', show_post, name='show_post'),
    path('add_post/', add_post, name='add_post'),
    path('like_post/', like_post, name='like_post'), # New URL for the like request  
    path('post_comment/', post_comment, name='post_comment'), # New URL for the like request   
 
]