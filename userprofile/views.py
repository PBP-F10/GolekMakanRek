from django.shortcuts import render
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, JsonResponse
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
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
@login_required(login_url='/authentication/login')
def show_user_profile_page(request):
    return render(request, "userprofile.html")

@login_required(login_url='/authentication/login')
def get_user_profile(request):
    # Ensure the user is authenticated and then get or create the UserProfile
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    print("user " + str(request.user.id))
    # Prepare profile data to send as JSON
    profile_data = {
        "username": profile.user.username,
        "description": profile.description,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "date_of_birth": profile.date_of_birth,
        "gender": profile.gender,
        "location": profile.location,
        "phone_number": profile.phone_number,
        "email": profile.email,
    }

    # Send profile data along with top games as JSON response
    return JsonResponse({
        "profile": profile_data,
        "created": created,
    })

@login_required(login_url='/authentication/login')
def update_user_profile(request):
    # Get the user's profile instance
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Bind form with the POST data and existing profile instance
    form = UserProfileForm(request.POST, instance=profile)

    # Validate the form
    if form.is_valid():
        # Save the updated profile data
        form.save()
        return JsonResponse({"message": "Profile updated successfully!"})
    else:
        # Combine errors into a single string
        error_messages = "\n".join(
            f"- {error[0]}" for field, error in form.errors.items()
        )
        return JsonResponse({"errors": error_messages}, status=400)

@csrf_exempt
def update_user_profile_flutter(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            
            # Validate the user existence
            user = request.user

            # Get or create the user's profile
            profile, created = UserProfile.objects.get_or_create(user=user)

            # Update the profile fields with data from the request
            profile.description = data.get("description", profile.description)
            profile.first_name = data.get("first_name", profile.first_name)
            profile.last_name = data.get("last_name", profile.last_name)
            profile.date_of_birth = data.get("date_of_birth", profile.date_of_birth)
            profile.gender = data.get("gender", profile.gender)
            profile.location = data.get("location", profile.location)
            profile.phone_number = data.get("phone_number", profile.phone_number)
            profile.email = data.get("email", profile.email)

            # Save the profile
            profile.save()

            print(profile)

            return JsonResponse({"status": "success", "message": "Profile updated successfully!"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)