from .models import show_resto, Rating, Follow
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def restaurant_preview(request):
    restaurants = show_resto.objects.all()
    followed_restaurants = Follow.objects.filter(user=request.user).values_list('restaurant_id', flat=True) if request.user.is_authenticated else []

    return render(request, 'show_preview.html', {
        'restaurants': restaurants,
        'followed_restaurants': followed_restaurants,
    })

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(show_resto, id=restaurant_id)  
    average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg'] or 0
    user_rating = None

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, restaurant=restaurant).first()
    
    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'user_rating': user_rating,
        'average_rating': average_rating, 
        'total_ratings': restaurant.total_ratings(), 
    })

@login_required
def submit_rating(request, restaurant_id):  
    if request.method == 'POST':
        score = request.POST.get('score')
        restaurant = get_object_or_404(show_resto, id=restaurant_id)

        user_rating = Rating.objects.filter(user=request.user, restaurant=restaurant).first()
        if user_rating:
            user_rating.score = score
            user_rating.save()
        else:
            Rating.objects.create(user=request.user, restaurant=restaurant, score=score)

        average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg'] or 0

        return JsonResponse({
            'average_rating': average_rating,
            'user_rating': score,  
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def follow_restaurant(request, restaurant_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            restaurant = get_object_or_404(show_resto, id=restaurant_id)
            Follow.objects.get_or_create(user=request.user, restaurant=restaurant)
            return redirect('resto_preview:restaurant_detail', restaurant_id=restaurant_id)
        else:
            return redirect('resto_preview:show_preview', alert="Silakan login untuk mengikuti restoran.")
    return redirect('resto_preview:show_preview')
