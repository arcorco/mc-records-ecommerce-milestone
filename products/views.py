from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Track
from .filters import ProductFilter
import random

# Create your views here.


def all_products(request):
    product_list = Product.objects.all()
    artist_list = Product.objects.values_list('artist', flat=True).distinct()

   
    artist = request.GET.get('artist')
    genre = request.GET.get('genre')
    decade = request.GET.get('decade')

    if is_valid_queryparam(artist):
        product_list = product_list.filter(artist=artist)

    if is_valid_queryparam(genre):
        product_list = product_list.filter(genre=genre)

    if is_valid_queryparam(decade):
        product_list = product_list.filter(
            release_date__range=[decade+'-01-01', str(int(decade)+10)+'-01-01'])
    
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "products.html", {"products": products, 'artist_list': artist_list,
         'genres': Product.GENRE_CHOICES, 'decades': [1970, 1980, 1990, 2000, 2010, 2020]})


def is_valid_queryparam(param):
    return param != '' and param is not None


def product_filter(request):
    return all_products(product_list)



def product_detail(request, id):
    product_list = Product.objects.all()
    product_list_without_current = product_list.exclude(pk=id)
    product = get_object_or_404(Product, pk=id)
    tracks = Track.objects.filter(album=product.id)
    random_albums = random.sample(list(product_list_without_current), k=3)
    return render(request, 'product_page.html', {'product': product, 'tracks': tracks, 'random_albums': random_albums})
