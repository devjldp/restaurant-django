from django.shortcuts import render, get_object_or_404, redirect
#import messages
from django.contrib import messages
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
        messages.success(request, "Dish added to the cart successfully")
        save_cart(request, cart)

        # debugging purpose
        for dish_id, quantity in cart.items(): # dictionary python -> how to print keys and values form a dictionary
            print(f"ID:{dish_id} - Quantity: {quantity}")

    except Exception as e:
        messages.error(request, "The dish could not be added to the cart.")
        print(f"Theres was an error: {e}")

    # redirect to
    return redirect('menu:menu_list')


def display_cart(request):
    # Get the cart
    cart = get_cart(request)

    # Get a list with the dish ids in our cart -> keys
    dish_ids = cart.Keys() # returns a list with all keys in the dictionary

    # Query the database
    dishes = MenuItem.objects.filter(id__in=dish_ids)
    # Create an empty list to store data. Each element in the list will be a dictionary
    cart_dishes =[]
    for dish in dishes:
        dish_data={
            'dish_data': dish, #dish is an object type MenuItem
            'quanty': cart[str(dish.id)],
            'total_price': dish.price * cart[str(dish.id)]
        }
        cart_dishes.append(dish_data)
    
    context = {
        'cart_dishes': cart_dishes
    }

    return render(request, 'cart_detail.html', context)
