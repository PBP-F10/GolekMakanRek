import datetime
from django.shortcuts import render, redirect, reverse
from .forms import SearchFoodForm, SearchRestaurantForm, LikeForm
from .models import Food, Restaurant, Likes
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib.auth.models import User

# Create your views here.
def show_homepage(request):
    food_search = SearchFoodForm()
    restaurant_search = SearchRestaurantForm()
    like = LikeForm()
    login(request, User.objects.get(username='joshua'))
    context = {
        'food_search': food_search,
        'restaurant_search': restaurant_search,
        'like_form': like,
        'likes': Likes.objects.filter(user_id=request.user) if request.user.is_authenticated else None,
        'foods': Food.objects.all(),
        'restaurants': Restaurant.objects.all()
    }
    return render(request, "index.html", context)

def search(request, type):
    if type == 'food':
        search_form = SearchFoodForm()
    else:
        search_form = SearchRestaurantForm()
    return HttpResponse(b"OK", status=200)

@login_required(login_url='/login')
@require_POST
@csrf_exempt
def toggle_like(request):
    try:
        like = Likes.objects.get(user_id=request.user, food_id=request.POST.get("food_id"))
    except Exception as e:
        like = None

    if like:
        like.delete()
        return HttpResponseRedirect(reverse("homepage:show_homepage"))

    like_form = LikeForm(request.POST)
    print(like_form.as_table())
    if like_form.is_valid() and like_form.cleaned_data["user_id"] == request.user:
        like = like_form.save(commit=False)
        like.save()
        return HttpResponseRedirect(reverse("homepage:show_homepage"))

def get_food(request):
    if request.GET:
        filters = {}
        for param in request.GET:
            if request.GET.get(param) != "None":
                filters[f"{param}__icontains"] = request.GET.get(param)
        data = serializers.serialize("json", Food.objects.filter(**filters))
        return HttpResponse(data, content_type="application/json")

    data = serializers.serialize("json", Food.objects.all())
    return HttpResponse(data, content_type="application/json")

def get_restaurant(request):
    if request.GET:
        filters = {}
        for param in request.GET:
            if request.GET.get(param) != "None":
                filters[f"{param}__icontains"] = request.GET.get(param)
        data = serializers.serialize("json", Restaurant.objects.filter(**filters))
        return HttpResponse(data, content_type="application/json")
    
    data = serializers.serialize("json", Restaurant.objects.all())
    return HttpResponse(data, content_type="application/json")