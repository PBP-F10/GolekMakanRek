from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "description",
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'gender', 
            'location', 
            'phone_number', 
            'email', 
        ]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone number should contain only digits.")
        return phone_number
