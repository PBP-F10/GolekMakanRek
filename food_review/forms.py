from django import forms
from .models import *

class FoodRatingForm(forms.ModelForm):
    class Meta:
        model = FoodRating
        fields = ['score', 'comment']