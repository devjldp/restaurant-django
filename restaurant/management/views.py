from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

#import messages
from django.contrib import messages

# import models:
from menu.models import MenuItem
from bookings.models import Booking

# import forms from menu app
from menu.forms import MenuItemForm
from bookings.forms import BookingForm, UpdateBookingForm

# Create your views here.
@login_required
def post_login_redirect(request):
    """
    Redirect users based on their role.
    """
    user = request.user
    # If statement to redirect user
    if user.is_superuser:
        # redirect to dashboard
        return redirect('management:home')
    else: 
        # regular customers -> to landing page
        return redirect('customers:create_profile')


@login_required
def management_home(request):
    """
    Render the dashboard only for superusers
    """
    if not request.user.is_superuser:
        return redirect('home:index')


    dashboard_items = [
        {"item": "menu", "image_url": "management/images/admin_menu.png", "url": reverse("management:list_dishes")},
        {"item": "bookings", "image_url": "management/images/admin_bookings.png", "url": reverse("management:list_reservations")},
        {"item": "orders", "image_url": "management/images/admin_orders.png", "url": "#" },
        {"item": "customers", "image_url": "management/images/admin_users.png", "url": "#"}
    ]    
    return render(request, 'dashboard.html', {'dashboard_items':dashboard_items})


# Implement the CRUD using Django ORM

# Menu management CRUD 

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
            messages.success(request, "Dish added successfully")
            return redirect('management:list_dishes')
        except Exception as e:
            print(f"There is an error inserting a new dish: {e}")
            messages.error(request, "There was an error creating a new dish")
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
        # implement remove image funcionality
        
        messages.success(request, "Dish deleted successfully")
    except Exception as e:
        print(f"There is an error deleting the dish: {e}")
        messages.error(request, "There was an error deleting a new dish")
    
    return redirect('management:list_dishes')

 # Create the view to update the price of a dish

@login_required
def management_update_dish(request, dish_id):

    dish = get_object_or_404(MenuItem, id=dish_id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=dish)
        # check if your form is valid
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Dish was updated")
                return redirect('management:list_dishes')
            except Exception as e:
                print(f"There is an error updating the dish: {e}")
                messages.error(request, "There was an error updating the dish")
        else:
            messages.warning(request, "Please correct the mistakes you have in the form.")
    else:
        form = MenuItemForm(instance=dish)
    
    # context ={
    #     'form':form,
    #     'dish':dish
    # }
    return render(request, 'dashboard_update_dish.html', {'form':form, 'dish':dish})

# Bookins management CRUD

@login_required
def management_display_reservations(request):
    # Get all object(books) in the system   
    # Use try and except to improve how to handle errors
    try:
        reservations = Booking.objects.all()
        print(reservations)
    except Exception as e:
        print(f"There is an error retrieving data: {e}")

    context = {
        'reservations': reservations
    }

    return render(request, 'dashboard_reservations.html', context)

@login_required
def management_complete_reservation(request,reservation_id):
    """
    Mark a reservation as completed.

    Args:
        request: HTTP request.
        reservation_id: ID of the reservation to complete.

    Returns:
        Redirects to the reservations list after updating the status.
    """
    try:
        reservation = get_object_or_404(Booking, id=reservation_id)
        reservation.status = 'completed'
        reservation.save()
        messages.success( request, f"Reservation with ID {reservation_id} was successfully completed.")

    except Exception as e:
        print(f"There is an error completing the reservation: {e}")
        mesage.error(reuqest, "There was an error completing the reservation")
    
    return redirect('management:list_reservations')

@login_required
def management_cancell_reservation(request,reservation_id):
    """
    Mark a reservation as cancelled.

    Args:
        request: HTTP request.
        reservation_id: ID of the reservation to complete.

    Returns:
        Redirects to the reservations list after updating the status.
    """
    try:
        reservation = get_object_or_404(Booking, id=reservation_id)
        reservation.status = 'cancelled'
        reservation.save()
        messages.success( request, f"Reservation with ID {reservation_id} was successfully cancelled.")

    except Exception as e:
        print(f"There is an error completing the reservation: {e}")
        mesage.error(reuqest, "There was an error completing the reservation")
    
    return redirect('management:list_reservations')

@login_required
def management_update_reservation(request, reservation_id):
    """ 
    Update an existing reservation from the management dashboard. Retrieves the reservation identified by reservation_id and displays it 
    in an UpdateBookingForm. 
    If the request is a POST request, the submitted form is validated and, if valid, the reservation is updated. 
    
    Args: 
        request (HttpRequest): The HTTP request sent by the user. 
        reservation_id (int): The ID of the reservation to update. 
    
    Returns: 
        HttpResponse: 
            - Redirects to the reservation list after a successful update. 
            - Renders the update reservation template with the form and reservation if the request is GET or the form is invalid. 
            
    Raises: 
        Http404: If no reservation exists with the given reservation_id. 
    """
    
    reservation = get_object_or_404(Booking, id=reservation_id)

    if request.method == 'POST':
        form = UpdateBookingForm(request.POST, instance=reservation)
        # check if your form is valid
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Reservation was successfully updated")
                return redirect('management:list_reservations')
            except Exception as e:
                print(f"There is an error updating the dish: {e}")
                messages.error(request, f"There was an error updating the reservation with ID {reservation_id}")
        else:
            messages.warning(request, "Please correct the mistakes you have in the form.")
    else:
        form = UpdateBookingForm(instance=reservation)
    
    return render(request, 'dashboard_update_reservation.html', {'form':form, 'reservation':reservation})    