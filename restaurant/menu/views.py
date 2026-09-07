from django.shortcuts import render

# import errors:
from django.db import DatabaseError
from django.http import JsonResponse

# import forms
from .forms import IngredientForm

# Import the models we are going to use
from .models import MenuItem, Category, Ingredient
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
        categories = Category.objects.all()
        # var1 = data from table1
        # var2 = data from table2
        # for debugging
        print(f"Retrieved {dishes.count()} from Database")
        print(f"Retrieved {categories.count()} from Database")
        
    except DatabaseError as e:
        print(f"There is an error in the query. Error: {e}")
        dishes = []
        categories = []
    
    context = {
        'menu': dishes,
        'categories': categories
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

def search_ingredients(request):
    """
    Search for ingredients whose name contains the search term.

    The search term is received through the 'q' GET parameter.
    The function returns a maximum of 30 matching ingredients
    as a JSON response.

    Args:
        request: HTTP request containing the search query.

    Returns:
        JsonResponse: A JSON list containing the ID and name
        of each matching ingredient. If a database error occurs,
        an error message is returned as JSON.
    """
    query = request.GET.get('q', '').strip()

    try:
        ingredients = Ingredient.objects.filter(
            name__icontains=query
        ).order_by('name')[:30]

        results = [
            {
                'id': ingredient.id,
                'name': ingredient.name,
            }
            for ingredient in ingredients
        ]

        return JsonResponse(results, safe=False)

    except DatabaseError as e:
        print(f"There is an error searching for ingredients: {e}")

        return JsonResponse(
            {
                'error': 'There was an error searching for ingredients.'
            },
            status=500
        )    

def create_ingredient(request):
    """
    Create a new ingredient and return its data as JSON.

    Args:
        request: HTTP request containing the new ingredient name.

    Returns:
        JsonResponse: The ID and name of the newly created ingredient,
            or validation/database errors.
    """
    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Only POST requests are allowed.'},
            status=405
        )

    form = IngredientForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {'errors': form.errors},
            status=400
        )

    try:
        ingredient = form.save()

        return JsonResponse({
            'id': ingredient.id,
            'name': ingredient.name,
        }, status=201)

    except DatabaseError as e:
        print(f"There is an error creating the ingredient: {e}")

        return JsonResponse(
            {
                'error': 'There was an error creating the ingredient.'
            },
            status=500
        )