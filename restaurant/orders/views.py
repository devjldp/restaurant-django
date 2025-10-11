from django.shortcuts import render, redirect
from django.contrib import messages


from .models import Order, Order_MenuItem
from menu.models import MenuItem
from customers.models import CustomerProfile

# import cart utils
from cart.utils import get_cart, save_cart


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

    # Context
    context = {
        'customer': customer,
        'order': order,
        'order_products': order.order_products.all()
    }

    return render(request, 'checkout.html', context)
