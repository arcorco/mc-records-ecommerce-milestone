from django.conf.urls import url
from .views import checkout, order

urlpatterns = [
    url(r'^$', checkout, name="checkout"),
    url(r'^order/', order, name="order")
]