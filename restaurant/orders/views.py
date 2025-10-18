from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from .models import Order, Order_MenuItem
from menu.models import MenuItem
from customers.models import CustomerProfile

# import cart utils
from cart.utils import get_cart, save_cart

# import forms
from .forms import OrderForm

#import stripe
import stripe

# Create your views here.

def create_order(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('account_login')
    
    cart = get_cart(request)

    if not cart: # true if the cart is empty
        messages.warning(request, "Please add product to your cart!")
        return redirect('menu:menu_list')
    
    # Get the customer lloged
    customer = CustomerProfile.objects.get(user_id = user.id)
    order = Order.objects.create( # Automatically save the order in the database
        customer = customer,
        total = 0
    )

    # Insert the dishesh for the cart in the table Order_MenuItem
    for dish_id, quantity in cart.items():
        # Get the product using the primary key: id
        product = MenuItem.objects.get(pk=dish_id)
        # Create the object in the table Order_MenuItem
        order_item = Order_MenuItem.objects.create(
            order_id = order,
            product_id = product,
            quantity = quantity,
            price = product.price
        )
    
    # Calculate the total
    total_products = sum(item.quantity*item.price for item in Order_MenuItem.objects.filter(order_id=order))
    # Update the total field in the order object
    order.total = total_products
    order.save()
    # Create the form object -> instance of OrderForm , pass as parameter the object customer
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=customer)
    else:
        form = OrderForm(instance=customer) 
    # Context
    context = {
        'customer': customer,
        'order': order,
        'order_products': order.order_products.all(),
        'order_form': form
    }

    return render(request, 'checkout.html', context)



def create_stripe_checkout(order):
    line_items = []
    for item in order.order_products.all():
        line_items.append({
            'price_data':{
                'currency': 'gbp',
                'unit_amout':int(item.price*100),
                'product_data':{
                    'name':item.product_id.name
                }
            },
            'quantity': item.quantity
        })
    
    # urls: success payment and cancell payment
    success_url = settings.SITE_URL + reverse() # define reverse path
    cancel_url = settings.SITE_URL + reverse()

    # Write the code to create the session => checkout
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url 
    )

    return checkout_session


def pay_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instace= order.customer)
        # validate the form
        if form.is_valid():
            form.save()
            checkout_stripe_session = create_stripe_checkout(order)

            # redirect the website to stripe website to pay
            return redirect(checkout_stripe_session.url)
    else:
        form = OrderForm(instance = order.customer)
    
    context ={
        'order': order,
        'order_form': form
    }
    return render(request, 'checkout.html', context)
    # return render(request, 'checkout.html', {'order': order, 'order_form' :form})

    # if the payment is success 
def payment_succes(request, order_id):
    order = Order.objects.get(pk = order_id)

    if order.status != Order.Status.PROCESSED:
        order.status = Order.status.PROCESSED
        order.save()

    return render(request, 'payment_success.html', {'order': order})

def payment_cancel(request, order_id):
    order = Order.objects.get(pk = order_id)

    if order.status == Order.Status.PENDING:
        order.status = Order.status.CANCELLED
        order.save()

    return render(request, 'payment_cancel.html', {'order': order})