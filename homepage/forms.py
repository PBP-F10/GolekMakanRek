from django.forms import *
# from .models import Food
# from .models import Restaurant
from .models import Food, Restaurant, Likes
from django.utils.html import strip_tags

class SearchFoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ["name", "category", "price"]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control form-control-border', 'placeholder': 'Masukkan nama makanan'}),
            'category': Select(attrs={'class': 'form-control form-control-border'}, choices=[('None', 'Pilih kategori')] + list(Food.objects.values_list('category', 'category').distinct())),
        }
        labels = {
            'name': 'Nama makanan',
            'category': 'Kategori',
            'price': 'Harga Makanan'
        }

    def __init__(self, *args, **kwargs):
        super(SearchFoodForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['category'].required = False
        self.fields['price'].required = False

    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

class SearchRestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "category"]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control form-control-border', 'placeholder': 'Masukkan nama restoran'}),
            'category': Select(attrs={'class': 'form-control form-control-border'}, choices= [('None', 'Pilih kategori')] + list(Restaurant.objects.values_list('category', 'category').distinct())),
        }
        labels = {
            'name': 'Nama Restoran',
            'category': 'Kategori',
        }
    
    def __init__(self, *args, **kwargs):
        super(SearchRestaurantForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['category'].required = False

    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

class LikeForm(ModelForm):
    class Meta:
        model = Likes
        fields = ["user_id" , "food_id"]
        widgets = {
            'food_id': HiddenInput(),
        }