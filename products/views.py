from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Track
from .filters import ProductFilter
import random

# Create your views here.
def is_valid_queryparam(param):
    return param != '' and param != [] and param is not None

def all_products(request):
    product_list = Product.objects.all()
    artist_list = Product.objects.values_list('artist', flat=True).distinct()
    artist = request.GET.getlist('artist')
    genre = request.GET.getlist('genre')
    decade = request.GET.get('decade')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    print(artist)

    if is_valid_queryparam(artist):
        product_list = product_list.filter(artist__in=artist)

    if is_valid_queryparam(genre):
        product_list = product_list.filter(genre__in=genre)

    if is_valid_queryparam(decade):
        product_list = product_list.filter(
            release_date__range=[decade+'-01-01', str(int(decade)+10)+'-01-01'])
    
    if is_valid_queryparam(price_min):
        product_list = product_list.filter(price__gte=float(price_min))
    
    if is_valid_queryparam(price_max):
        product_list = product_list.filter(price__lt=float(price_max))
    
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

def product_detail(request, id):
    product_list = Product.objects.all()
    product_list_without_current = product_list.exclude(pk=id)
    product = get_object_or_404(Product, pk=id)
    tracks = Track.objects.filter(album=product.id)
    random_albums = random.sample(list(product_list_without_current), k=3)
    return render(request, 'product_page.html', {'product': product, 'tracks': tracks, 'random_albums': random_albums})
