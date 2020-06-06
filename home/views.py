from django.shortcuts import render
from products.models import Product

# Create your views here.

def index(request):
    """A view that displays the home page"""
    products = Product.objects.all()
    recently_released = Product.objects.order_by('-release_date').all()[:3]
    return render(request, 'home.html',{"products": products, "recently_released": recently_released})