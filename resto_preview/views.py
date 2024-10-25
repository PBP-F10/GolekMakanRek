from .models import Restaurant, Rating
from django.shortcuts import render, get_object_or_404, redirect
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

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        # Cek jika pengguna sudah memberikan rating sebelumnya, jika ada, update
        user_rating = Rating.objects.filter(user=request.user, restaurant=restaurant).first()
        if user_rating:
            user_rating.score = score
            user_rating.save()
        else:
            # Jika belum ada, buat rating baru
            Rating.objects.create(user=request.user, restaurant=restaurant, score=score)

        # Redirect kembali ke halaman detail restoran
        return redirect('resto_preview:restaurant_detail', restaurant_id=restaurant.id)

    return JsonResponse({'error': 'Invalid request'}, status=400)
