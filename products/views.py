from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Track
import random

# Create your views here.

def all_products(request):
    product_list = Product.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "products.html", {"products": products})

def product_detail(request, id):
    product_list = Product.objects.all()
    product_list_without_current = product_list.exclude(pk=id)
    product = get_object_or_404(Product, pk=id)
    tracks = Track.objects.filter(album=product.id)
    random_albums = random.sample(list(product_list_without_current), k=3)
    return render(request, 'product_page.html', {'product': product, 'tracks': tracks, 'random_albums': random_albums})