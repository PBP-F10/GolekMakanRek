from django.urls    import path
from .              import views

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

    path('foodrating_json/', views.foodrating_json, name='food_rating'),

    path('wishlist/toggle/<uuid:food_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist, name='show_wishlist'),
    path('wishlist/status/', views.get_wishlist_status, name='get_wishlist_status'),
    path('wishlist/json/', views.wishlist_json, name='wishlist_json'),
    path('wishlist/check/', views.check_wishlist_items, name='check_wishlist_items'),
]
