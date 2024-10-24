from django.shortcuts import render, redirect, reverse
from .forms import SearchFoodForm, SearchRestaurantForm, LikeForm
from main.models import Food, Restaurant
from .models import Likes
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib.auth.models import User
import json
import os

# Create your views here.
def show_homepage(request):
    food_search = SearchFoodForm()
    restaurant_search = SearchRestaurantForm()
    # login(request, User.objects.get(username='joshua')) # hapus nanti kalau udah ada auth
    # logout(request)
    context = {
        'food_search': food_search,
        'restaurant_search': restaurant_search,
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
        return HttpResponse(b"Unliked!", 201)

    like_form = LikeForm(request.POST)
    if like_form.is_valid() and like_form.cleaned_data["user_id"] == request.user:
        like_form.save()
        return HttpResponse(b"Liked!", 201)
    print(like_form.errors)
    return HttpResponse(b"Invalid form", status=400)

def get_food(request):
    if request.GET:
        filters = {}
        like_only = False
        for param in request.GET:
            if param == "like_filter":
                like_only = True
                continue
            if request.GET.get(param) != "None":
                filters[f"{param}__icontains"] = request.GET.get(param)
        if like_only:
            data = serializers.serialize("json", Food.objects.filter(**filters).filter(likes__user_id=request.user))
            return HttpResponse(data, content_type="application/json")
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

@login_required(login_url='/login')
def get_likes(request):
    if request.user.is_authenticated:
        data = serializers.serialize("json", Likes.objects.filter(user_id=request.user))
        return HttpResponse(data, content_type="application/json")

# hanya untuk test
'''
def set_test(request):
    Restaurant.objects.all().delete()
    Food.objects.all().delete()
    file_path_1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "merchant_gofood_dataset.json")
    with open(file_path_1, "r") as json_file:
        data = json.load(json_file)
        for restaurant in data:
            new_restaurant = Restaurant.objects.create(
                nama=restaurant['fields']['nama'],
                kategori=restaurant['fields']['kategori'],
                deskripsi=restaurant['fields']['deskripsi'],
            )
            new_restaurant.save()
    file_path_2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gofood_dataset.json")
    with open(file_path_2, "r") as json_file:
        data = json.load(json_file)
        for food in data:
            new_food = Food.objects.create(
                nama=food['product'],
                kategori=food['category'],
                harga=food['price'],
                diskon=food['discount_price'] if food['discount_price'] else 0,
                deskripsi=food['description'],
                restoran=Restaurant.objects.get(nama=food['merchant_name'])
            )
            new_food.save()
    return HttpResponseRedirect(reverse('homepage:show_homepage'))
'''