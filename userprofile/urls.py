from django.urls import path
from userprofile.views import *

app_name = 'userprofile'

urlpatterns = [
    path('userprofile/', show_user_profile, name='userprofile')
]