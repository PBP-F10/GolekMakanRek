from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout')
]