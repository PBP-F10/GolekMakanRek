from django.urls import path
from .views import show_post, add_post
app_name = 'forum'

urlpatterns = [
    path('', show_post, name='show_post'),
    path('add_post/', add_post, name='add_post')
]