from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from wishlist.models import Wishlist
import json

# Create your views here.
def show_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        "wishlist": wishlist
    }

    ## Ini untuk ngetes ##
    # f = open('gofood_dataset.json')
    # p = json.load(f)
    # f.close()
    # context = {
    #     "wishlist": p
    # }

    return render(request, 'wishlist.html', context)

def delete_item(request, id):
    item = Wishlist.objects.get(pk=id)
    item.delete()
    return HttpResponseRedirect(reverse('main:show_main'))