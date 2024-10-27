from .models import Restaurant, Rating
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main.models import *

def restaurant_preview(request):
    restaurants = Restaurant.objects.all()  
    return render(request, 'show_preview.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)  
    user_rating = None
    
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, restaurant=restaurant).first()
    
    average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg'] or 0
    restaurant_foods = Food.objects.filter(restoran=restaurant)

    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'user_rating': user_rating,
        'average_rating': average_rating,
        'foods': restaurant_foods,
    })

@login_required
def submit_rating(request, restaurant_id):
    if request.method == 'POST':
        score = request.POST.get('score')

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)  

        user_rating = Rating.objects.filter(user=request.user, restaurant=restaurant).first()
        if user_rating:
            user_rating.score = score
            user_rating.save()
        else:
            Rating.objects.create(user=request.user, restaurant=restaurant, score=score)

        return JsonResponse({'message': 'Rating submitted successfully', 'average_rating': restaurant.rating_set.aggregate(Avg('score'))['score__avg']}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)