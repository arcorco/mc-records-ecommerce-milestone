from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from decimal import Decimal
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse
from products.models import Product
from checkout.models import Order, OrderLineItem
import stripe


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def checkout(request):
    """Renders checkout page with form for user to purchase prodcuts using Stripe API"""
    cart = request.session.get('cart', {})
    total = 0
    for id, quantity in cart.items():
        product = get_object_or_404(Product, pk=id)  
        total += quantity * product.price
    delivery = 0
    if total > 30:
        delivery = 0
    else:
        delivery = 3.95
    new_total =  round(float(total) + delivery, 2)

    if request.method=="POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.purchased_by = request.user
            order.date = timezone.now()
            order.save()

            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)  
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order = order,
                    product = product, 
                    quantity = quantity
                )
                order_line_item.save()
            try:
                customer = stripe.Charge.create(
                    amount = int(new_total * 100),
                    currency = "GBP",
                    description = request.user.email,
                    card = payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.error(request, "You have successfully paid!")
                request.session['cart'] = {}
                return redirect(reverse('confirmation', args=(order.id,)))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
    
    return render(request, "checkout.html", {"order_form": order_form, "payment_form": payment_form, "delivery": delivery, "new_total": new_total, "publishable":settings.STRIPE_PUBLISHABLE})

@login_required()
def confirmation(request, id):
    """Renders user confirmation page to showing an order summary"""
    order = Order.objects.get(id=id)
    purchases = OrderLineItem.objects.filter(order_id=id)
    user = User.objects.get(email=request.user.email)
    if order.purchased_by != request.user.username:
        return render(request, "403.html")
    totals = []
    total = 0
    for purchase in purchases:
        if purchase.order_id == order.id:
            total += purchase.product.price*purchase.quantity
            totals.append((purchase.order_id, float(total)))
            total=0
    order_total=[]
    value=0
    for t in totals:
        value += t[1]
    order_total.append((t[0], value))
    delivery = 0
    if order_total[0][1] > 30:
        delivery = 0
    else:
        delivery = 3.95
    
    final_total = round(order_total[0][1] + delivery, 2)

    return render(request, "confirmation.html", {'order': order, "profile": user, "purchases": purchases, "final_total": final_total})
        