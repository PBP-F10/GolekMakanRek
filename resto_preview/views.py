from django.shortcuts import render
from .models import Restaurant
from django.shortcuts import get_object_or_404, redirect

def restaurant_preview(request):
    restaurants = Restaurant.objects.all()  
    return render(request, 'show_preview.html', {'restaurants': restaurants})

def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        
    })
