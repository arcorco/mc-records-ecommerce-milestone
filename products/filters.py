from django import forms
import datetime
from django_filters import FilterSet, MultipleChoiceFilter
from .models import Product

artists = Product.objects.values_list('artist', flat=True).distinct()
artists_list = []
for i in range(0, len(artists)):
    artists_list.append([artists[i], artists[i]])

class ProductFilter(FilterSet):
    artist = MultipleChoiceFilter(field_name="artist", choices=artists_list)
    genre = MultipleChoiceFilter(field_name="genre", choices=Product.GENRE_CHOICES)
    
    class Meta:
        model = Product
        fields = ['genre', 'artist']




      
        