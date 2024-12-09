from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Pastikan kamu mengimpor User
from authentication.models import UserProfile  # Impor UserProfile dari aplikasi authentication

class UserProfileForm(UserCreationForm):
    nickname = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    age = forms.IntegerField(required=True)
    region = forms.CharField(required=True)

    class Meta:
        model = User  # Gunakan User di Meta
        fields = ['username', 'password1', 'password2', 'nickname', 'phone', 'age', 'region']  # Gunakan username dari model User

    def save(self, commit=True):
        user = super().save(commit=False)
        user_profile = UserProfile(
            user=user,
            nickname=self.cleaned_data['nickname'],
            phone=self.cleaned_data['phone'],
            age=self.cleaned_data['age'],
            region=self.cleaned_data['region'],
        )
        if commit:
            user.save()
            user_profile.save()
        return user
