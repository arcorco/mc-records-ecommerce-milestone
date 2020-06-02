from django.conf.urls import url
from .views import checkout, confirmation

urlpatterns = [
    url(r'^$', checkout, name="checkout"),
    url(r'^confirmation/(?P<id>\d+)', confirmation, name="confirmation")

]