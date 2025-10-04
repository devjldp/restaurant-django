from django.shortcuts import render, get_object_or_404, redirect

# import models
from menu.models import MenuItem

# import the utils
from .utils import get_cart, save_cart

# Create your views here.

def add_to_cart(request, dish_id):
    """
    Add a new dish to the cart
    redirect to menu_list url
    """
    try:

        # securtity check: If the dish_id -> object (menuItem) exists in the database
        dish = get_object_or_404(MenuItem, pk=dish_id)

        cart = get_cart(request)
        # if we don't have any cart in our session we are creating an empty dictionary
        # if we have a previous cart -> returning the cart we creted previously with data stored.

        dish_id_str = str(dish_id) # transform dish_id number to string

        if dish_id_str in cart:
            cart[dish_id_str] += 1
        else:
            cart[dish_id_str] = 1
        
        save_cart(request, cart)

    except Exception as e:
        print(f"Theres was an error: {e}")

    # redirect to
    return redirect('menu:menu_list')
