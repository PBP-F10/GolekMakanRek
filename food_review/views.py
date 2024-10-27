from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main.models import *

def restaurant_preview(request):
    restaurants = Restaurant.objects.all()  
    return render(request, 'show_detail.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)  
    user_rating = None
    
    average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg'] or 0
    restaurant_foods = Food.objects.filter(restoran=restaurant)

    return render(request, 'food_list.html', {
        'restaurant': restaurant,
        'user_rating': user_rating,
        'average_rating': average_rating,
        'foods': restaurant_foods,
    })

@login_required
def add_rating(request, food_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        
    food = get_object_or_404(Food, id=food_id)
    score = request.POST.get('score')
    comment = request.POST.get('comment', '')
    
    try:
        score = int(score)
        if not (1 <= score <= 5):
            raise ValueError
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid rating score'})
        
    rating, created = FoodRating.objects.update_or_create(
        user=request.user,
        deskripsi_food=food,
        defaults={
            'score': score,
            'comment': comment
        }
    )
    
    return JsonResponse({
        'status': 'success',
        'message': 'Rating saved successfully'
    })

@login_required
def edit_rating(request, rating_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        
    rating = get_object_or_404(FoodRating, id=rating_id, user=request.user)
    score = request.POST.get('score')
    comment = request.POST.get('comment', '')
    
    try:
        score = int(score)
        if not (1 <= score <= 5):
            raise ValueError
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid rating score'})
        
    rating.score = score
    rating.comment = comment
    rating.save()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Rating updated successfully'
    })

@login_required
def delete_rating(request, rating_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        
    rating = get_object_or_404(FoodRating, id=rating_id, user=request.user)
    rating.delete()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Rating deleted successfully'
    })

def get_user_rating(request, food_id):
    if not request.user.is_authenticated:
        return JsonResponse({'has_rating': False})
        
    food = get_object_or_404(Food, id=food_id)
    rating = FoodRating.objects.filter(user=request.user, deskripsi_food=food).first()
    
    if rating:
        return JsonResponse({
            'has_rating': True,
            'rating_id': rating.id,
            'rating': rating.score,
            'comment': rating.comment
        })
    return JsonResponse({'has_rating': False})