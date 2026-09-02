from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking

# Create your views here.

def create_booking(request):
    """
    Handle table reservation requests.

    Pre-fills contact details if the user is authenticated and processes
    the booking form submission.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            
            messages.success( request, 'Your table reservation request has been submitted successfully!')
            return redirect('bookings:user_bookings')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['email'] = request.user.email
            
            # Pre-populate name and phone from CustomerProfile if available
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                full_name = f"{profile.first_name or ''} {profile.last_name or ''}".strip()
                initial_data['name'] = full_name or request.user.username
                initial_data['phone_number'] = getattr(profile, 'phone_number', '')
            else:
                initial_data['name'] = request.user.username

        form = BookingForm(initial=initial_data)

    return render(request, 'booking.html', {'form': form})

@login_required
def user_bookings(request):
    """
        Display a list of upcoming and past reservations for the authenticated customer.
    """
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    """
    Allow an authenticated customer to cancel their own reservation.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your reservation has been cancelled successfully.')
        return redirect('bookings:user_bookings')

    return render(request, 'booking_cancel_confirm.html', {'booking': booking})