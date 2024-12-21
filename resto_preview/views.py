from .models import Restaurant, Food, Rating, Follow
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

def restaurant_preview(request):
    restaurants = Restaurant.objects.all()
    followed_restaurants = Follow.objects.filter(user=request.user).values_list('restaurant_id', flat=True) if request.user.is_authenticated else []

    return render(request, 'show_preview.html', {
        'restaurants': restaurants,
        'followed_restaurants': followed_restaurants,
    })

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)  
    restaurant_foods = Food.objects.filter(restoran=restaurant)
    average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg'] or 0
    user_rating = None

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, restaurant=restaurant).first()

    total_ratings = Rating.objects.filter(restaurant=restaurant).count() 

    # print("user " + str(request.user.id))
    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'foods': restaurant_foods,
        'user_rating': user_rating,
        'average_rating': average_rating, 
        'total_ratings': total_ratings,
    })

@csrf_exempt
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

        average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg'] or 0

        return JsonResponse({
            'average_rating': average_rating,
            'user_rating': score,  
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def follow_restaurant(request, restaurant_id):
    if request.method == "POST":
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        follow = Follow.objects.get_or_create(user=request.user, restaurant=restaurant)
        if not follow:
            follow.delete()
    return redirect('resto_preview:restaurant_detail', restaurant_id=restaurant_id)

@csrf_exempt
@login_required
def unfollow_restaurant(request, restaurant_id):
    if request.method == "POST":
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        follow = Follow.objects.get(user=request.user, restaurant=restaurant)
        follow.delete() 

    return redirect('resto_preview:restaurant_detail', restaurant_id=restaurant_id)

def get_restaurant_rating(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    average_rating = restaurant.rating_set.aggregate(Avg('score'))['score__avg']
    total_ratings = Rating.objects.filter(restaurant=restaurant).count() 

    return JsonResponse({
        'has_rating': True,
        'restaurant_id': restaurant.id,
        'average_rating': average_rating if average_rating else 'No ratings yet',
        'total_ratings': total_ratings,
    })

    return serialize_data(request, Rating, "json")

def get_user_rating(request, restaurant_id):
    user_rating = Rating.objects.filter(user=request.user, restaurant=restaurant_id).first()
    
    return JsonResponse({
        'has_rating': True,
        'restaurant_id': restaurant_id,
        'user_rating': user_rating.score,
    })

    return serialize_data(request, Rating, "json")

def get_follow_status(request):
    list_follow = list(Follow.objects.filter(user=request.user).values_list('restaurant_id', flat=True))

    return JsonResponse({
        'has_follow': True,
        'followed_restaurant': list_follow,
    })
    
def serialize_data(request, model, fmt, id=None):
    if id:
        data = get_object_or_404(model, pk=id)
        data = [data]
    else:
        data = model.objects.all()
    return HttpResponse(serializers.serialize(fmt, data), content_type=f"application/{fmt}")

def restorating_json(request):
    return serialize_data(request, Rating, "json")

def restofollow_json(request):
    return serialize_data(request, Follow, "json")
