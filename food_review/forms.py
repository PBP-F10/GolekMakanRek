from django import forms
from ..main.models import Restaurant, Food
from .models import *

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['nama', 'kategori', 'deskripsi']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['nama', 'kategori', 'harga', 'diskon', 'deskripsi', 'restoran']

class FoodRatingForm(forms.ModelForm):
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1', 'max': '5'})
    )
    
    class Meta:
        model = FoodRating
        fields = ['rating', 'comment']