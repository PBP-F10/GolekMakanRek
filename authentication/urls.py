from django.urls import path
from authentication.views import login, register, logout, get_username

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('get_username/', get_username, name='get_username')
]