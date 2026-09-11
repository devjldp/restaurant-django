from django import forms
from .models import Booking
from datetime import date

class BookingForm(forms.ModelForm):
    """
    Form for customers to make a table reservation.
    
    Uses standard HTML5 input types (date, time) to ensure cross-browser 
    compatibility and includes Bootstrap classes for styling.
    """
    
    class Meta:
        model = Booking
        # fields excluded: user, status, created_at, updated_at (handled automatically or by admin)
        fields = ['name', 'email', 'phone_number', 'booking_date', 'booking_time', 'number_of_guests', 'special_requests']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email Address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Phone Number'
            }),
            'booking_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date', # Renders a calendar picker in the browser
                'min': date.today().isoformat() # Prevents booking in the past
            }),
            'booking_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time', # Renders a time picker in the browser
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 12,
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any dietary requirements or special occasions?'
            }),
        }

class UpdateBookingForm(forms.ModelForm):
    """
    Form used by managers to update an existing reservation.
    """

    class Meta:
        model = Booking
        fields = [
            'booking_date',
            'booking_time',
            'number_of_guests',
            'status'
        ]

        widgets = {
            'booking_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date', # Renders a calendar picker in the browser
                'min': date.today().isoformat() # Prevents booking in the past
            }),
            'booking_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time', # Renders a time picker in the browser
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 12,
            }),

        }