from django import forms
from .models import Rating, Follow

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["food", "score"]  

class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ["user", "restaurant"]  
        