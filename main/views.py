from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

def show_main(request):
    context = {
        'features': [
            {'title': 'Discover Culinary Delights'},
            {'title': 'User-Friendly Experience'},
            {'title': 'Local Insights and Recommendations'},
        ],
        'categories': [
            {'name': 'Lontong Balap', 'color': 'green', 'image': '../../static/img/homepage/lontongbalap.jpg'},
            {'name': 'Rujak Cingur', 'color': 'orange', 'image': '../../static/img/homepage/rujakcingur.jpg'},
            {'name': 'Sego Sambel', 'color': 'yellow', 'image': '../../static/img/homepage/segosambel.jpg'},
        ],
        'services': [
            {'title': 'Curated Food Listings', 'description': 'We handpick the best eateries and food stalls in Surabaya, ensuring you always have access to the tastiest and most authentic dishes the city has to offer.', 'icon': '../../static/img/homepage/cur.png'},
            {'title': 'Up-to-Date Information', 'description': 'Stay informed with the latest updates, including menus, pricing, and operating hours, so you can plan your food adventures without any surprises.', 'icon': '../../static/img/homepage/update.png'},
            {'title': 'Community Feedback', 'description': 'Benefit from real reviews and ratings by fellow food enthusiasts, helping you make informed decisions on where to eat.', 'icon': '../../static/img/homepage/feedback.png'},
        ],
    }
    return render(request, 'main.html', context)

def register_user(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("homepage:show_homepage"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

