from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

# import MenuItem model from menu app
from menu.models import MenuItem

# import forms from menu app
from menu.forms import MenuItemForm, UpdatePriceForm

# Create your views here.
@login_required
def post_login_redirect(request):
    """
    Redirectusers based on their role.
    """
    user = request.user
    # If statement to redirect user
    if user.is_superuser:
        # redirect to dashboard
        return redirect('management:home')
    else: 
        # regular customers -> to landing page
        return redirect('home:index')


@login_required
def management_home(request):
    """
    Render the dashboard only for superusers
    """
    if not request.user.is_superuser:
        return redirect('home:index')
    return render(request, 'dashboard.html')


# Implement the CRUD using Django ORM
# view to render all dishes - only the name of the dish

@login_required
def management_select_all_dishes(request):
    # Get all object(dishes) in the menu: -> we need to import the models.
    
    # Use try and except to improve how to handle errors
    try:
        dishes = MenuItem.objects.all()
    except Exception as e:
        print(f"There is an error retrieving data: {e}")

    context = {
        'menu': dishes
    }

    return render(request, 'dashboard_dishes.html', context)

@login_required
def management_add_dish(request):
    """
    View to add a new dish into the database.
    Handles GET and POST methods:
        - GET displays an empty MenuItemForm
        - POST validates the form and insert a new dish in the database.
    Args:
        - request
    returns:
        - Response renders the dashboard_add_dish.html template with the form.
    """
    if request.method == 'POST':
        # Get the information:
        form = MenuItemForm(request.POST, request.FILES)
        # insert data in the database
        try:
            form.save()
            return redirect('management:list_dishes')
        except Exception as e:
            print(f"There is an error inserting a new dish: {e}")
    else:
        form = MenuItemForm()
    return render(request, 'dashboard_add_dish.html', {'form': form })


@login_required
def management_delete_dish(request, dish_id):
    """
    Don't forget comment your methods / functions
    """
    # When we remove a dish we are going to select only one dish using id. #get and get_object_or_404
    try:
        dish = MenuItem.objects.get(id = dish_id)
        # dish = get_object_or_404(MenuItem, id=dish_id)
        dish.delete()
    except Exception as e:
        print(f"There is an error deleting the dish: {e}")
    
    return redirect('management:list_dishes')

 # Create the view to update the price of a dish

@login_required
def management_update_dish(request, dish_id):
    dish = get_object_or_404(MenuItem, id=dish_id)

    if request.method == 'POST':
        form = UpdatePriceForm(request.POST, instance=dish)
        # check if your form is valid
        if form.is_valid():
            try:
                form.save()
                return redirect('management:list_dishes')
            except Exception as e:
                print(f"There is an error updating the dish: {e}")
    else:
        form = UpdatePriceForm()
    
    # context ={
    #     'form':form,
    #     'dish':dish
    # }
    return render(request, 'dashboard_update_dish.html', {'form':form, 'dish':dish})