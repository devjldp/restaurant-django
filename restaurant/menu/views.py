from django.shortcuts import render

# import errors:
from django.db import DatabaseError


# Import the models we are going to use
from .models import MenuItem
# from home.models import  => importing form a different app

# Create your views here.
def select_all_menu(request):
    """
    This function retrieves all dishes from the database
    return menu template / dish data
    """
    try:
        # query = "Select * from menuITem inner join menuitem.catery = Category.id"
        # connection to the databse
        # cursor....
        dishes = MenuItem.objects.all()
        # var1 = data from table1
        # var2 = data from table2
        # for debugging
        print(f"Retrieved {dishes.count()} from Database")
    except DatabaseError as e:
        print(f"There is an error in the query. Error: {e}")
        dishes = []
    
    context = {
        'menu': dishes,
        #'customer' : var1
        #'order' : var2
    }
    return render(request, 'menu.html', context)


def menu_detail(request, dish_id):
    """
    This view retrieve a single dish form our database and its ingredients.
    """

    try:
        # I am retrieving a single object from table MenuItem
        dish = MenuItem.objects.get(id = dish_id)
        print(dish)
        # Using the object retrieved, we are gogint to retrieve all objects related to ingredients field
        ingredients = dish.ingredients.all()
    except DatabaseError as e:
        print(f"There is an error in the query. Error: {e}")
        dish = None
        ingredients = []
    
    # context
    context = {
        'item': dish,
        'ingredients': ingredients
    }

    return render(request, 'menu_detail.html', context)