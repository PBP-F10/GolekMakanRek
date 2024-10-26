from django.forms import *
# from .models import Food
# from .models import Restaurant
from main.models import Food, Restaurant
from .models import Likes
from django.utils.html import strip_tags

class SearchFoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ["nama", "kategori"]
        widgets = {
            'nama': TextInput(attrs={'class': 'form mt-2 w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'placeholder': 'Masukkan nama makanan'}),
            'kategori': Select(attrs={'class': 'form mt-2 block w-full px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
        }
        labels = {
            'nama': 'Nama Makanan',
            'kategori': 'Kategori',
        }

    def __init__(self, *args, **kwargs):
        super(SearchFoodForm, self).__init__(*args, **kwargs)
        self.fields['nama'].required = False
        self.fields['kategori'].required = False
        choices = [('None', 'Pilih kategori')]
        categories = Food.objects.values_list('kategori', flat=True).distinct()
        for category in categories:
            split_categories = category.split('/')
            for split_category in split_categories:
                if (split_category, split_category) not in choices:
                    choices.append((split_category, split_category))
        self.fields['kategori'].widget.choices = choices

    def clean_name(self):
        name = self.cleaned_data["nama"]
        return strip_tags(name)

class SearchRestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ["nama", "kategori"]
        widgets = {
            'nama': TextInput(attrs={'class': 'form mt-2 w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'placeholder': 'Masukkan nama restoran'}),
            'kategori': Select(attrs={'class': 'form mt-2 block w-full px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
        }
        labels = {
            'nama': 'Nama Restoran',
            'kategori': 'Kategori',
        }
    
    def __init__(self, *args, **kwargs):
        super(SearchRestaurantForm, self).__init__(*args, **kwargs)
        self.fields['nama'].required = False
        self.fields['kategori'].required = False
        choices = [('None', 'Pilih kategori')]
        categories = Restaurant.objects.values_list('kategori', flat=True).distinct()
        for category in categories:
            split_categories = category.split('/')
            for split_category in split_categories:
                if (split_category, split_category) not in choices:
                    choices.append((split_category, split_category))
        self.fields['kategori'].widget.choices = choices

    def clean_name(self):
        name = self.cleaned_data["nama"]
        return strip_tags(name)

class LikeForm(ModelForm):
    class Meta:
        model = Likes
        fields = ["user_id" , "food_id"]
        widgets = {
            'user_id': HiddenInput(),
            'food_id': HiddenInput(),
        }