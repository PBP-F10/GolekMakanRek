from .models import show_resto, Rating
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def restaurant_preview(request):
    restaurants = show_resto.objects.all()  
    return render(request, 'show_preview.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(show_resto, id=restaurant_id)  
    user_rating = None

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, restaurant=restaurant).first()
    
    average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg'] or 0

    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'user_rating': user_rating,
        'average_rating': average_rating,  
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

        return JsonResponse({'message': 'Rating submitted successfully', 'average_rating': restaurant.rating_set.aggregate(Avg('score'))['score__avg']}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)
