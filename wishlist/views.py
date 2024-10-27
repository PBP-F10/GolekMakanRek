from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from wishlist.models import Wishlist
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def show_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        "wishlist": wishlist
    }

    return render(request, 'wishlist.html', context)

@login_required
def delete_item(request, id):
    item = Wishlist.objects.get(pk=id)
    item.delete()
    return HttpResponseRedirect(reverse('main:show_main'))