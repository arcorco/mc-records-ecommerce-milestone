from django.conf.urls import url
from .views import all_products, product_detail, product_decades

urlpatterns = [
    url(r'^$', all_products, name="products"),
    url(r'^(?P<decade>\w+)$', product_decades, name="product_decades"),
    url(r'^details/(?P<id>\d+)$', product_detail, name="product_detail"),
]