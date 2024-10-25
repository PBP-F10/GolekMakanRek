from .models import Restaurant, Rating
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from django.http import JsonResponse

def restaurant_preview(request):
    restaurants = Restaurant.objects.all()  
    return render(request, 'show_preview.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    user_rating = None

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, restaurant=restaurant).first()
    
    average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg'] or 0

    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'user_rating': user_rating,
        'average_rating': average_rating,  
    })

def submit_rating(request):
    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        score = request.POST.get('score')

        if not score.isdigit() or int(score) < 1 or int(score) > 5:
            return JsonResponse({'error': 'Invalid score'}, status=400)

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        rating, created = Rating.objects.update_or_create(
            restaurant=restaurant,
            user=request.user,
            defaults={'score': int(score)}
        )

        average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg'] or 0

        return JsonResponse({
            'average_rating': average_rating,
            'user_rating': int(score), 
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)