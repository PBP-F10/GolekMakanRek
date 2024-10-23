from django.forms import *
# from .models import Food
# from .models import Restaurant
from main.models import Food, Restaurant
from .models import Likes
from django.utils.html import strip_tags

class SearchFoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ["nama", "kategori", "harga"]
        widgets = {
            'nama': TextInput(attrs={'class': 'form-control form-control-border', 'placeholder': 'Masukkan nama makanan'}),
            'kategori': Select(attrs={'class': 'form-control form-control-border'}, choices=[('None', 'Pilih kategori')] + list(Food.objects.values_list('kategori', 'kategori').distinct())),
        }
        labels = {
            'nama': 'Nama Makanan',
            'kategori': 'Kategori',
            'harga': 'Harga Makanan'
        }

    def __init__(self, *args, **kwargs):
        super(SearchFoodForm, self).__init__(*args, **kwargs)
        self.fields['nama'].required = False
        self.fields['kategori'].required = False
        self.fields['harga'].required = False

    def clean_name(self):
        name = self.cleaned_data["nama"]
        return strip_tags(name)

class SearchRestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ["nama", "kategori"]
        widgets = {
            'nama': TextInput(attrs={'class': 'form-control form-control-border', 'placeholder': 'Masukkan nama restoran'}),
            'kategori': Select(attrs={'class': 'form-control form-control-border'}, choices= [('None', 'Pilih kategori')] + list(Restaurant.objects.values_list('kategori', 'kategori').distinct())),
        }
        labels = {
            'nama': 'Nama Restoran',
            'kategori': 'Kategori',
        }
    
    def __init__(self, *args, **kwargs):
        super(SearchRestaurantForm, self).__init__(*args, **kwargs)
        self.fields['nama'].required = False
        self.fields['kategori'].required = False

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