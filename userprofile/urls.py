from django.urls import path
from userprofile.views import *

app_name = 'userprofile'

urlpatterns = [
    path('', show_user_profile_page, name='userprofile'),    
    path('update/', update_user_profile, name="update_user_profile"),
    path('get/', get_user_profile, name="get_user_profile")
]