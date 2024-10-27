from django.urls import path
from . import views

app_name = 'food_review'

urlpatterns = [
    path('', views.restaurant_preview, name='foods'),
    path('<uuid:restaurant_id>/', views.restaurant_detail, name='restaurant_food'), 
    
    path('add-rating/<uuid:food_id>/', views.add_rating, name='add_rating'),
    path('edit-rating/<uuid:rating_id>/', views.edit_rating, name='edit_rating'),
    path('delete-rating/<uuid:rating_id>/', views.delete_rating, name='delete_rating'),
    path('get-user-rating/<uuid:food_id>/', views.get_user_rating, name='get_user_rating'),

    path('food/<uuid:food_id>/comments/', views.get_comments, name='get_comments'),
    path('food/<uuid:food_id>/comment/', views.add_comment, name='add_comment'),
]
