from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Booking(models.Model):
    """
    Represents a table reservation made by a customer.

    Stores details regarding reservation date, time, group size, and current status.
    An optional relationship with a registered user profile enables customers to view 
    and manage their bookings, whilst direct contact fields allow guest reservations.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Optional connection to an authenticated user account.
    # SET_NULL retains historical booking records if an account is deleted.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='bookings',
        null=True,
        blank=True
    )

    # Optional connection to an authenticated user account.
    # SET_NULL retains historical booking records if an account is deleted.
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='bookings', null=True, blank=True)

    # Direct contact details for both registered users and guest diners
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    # Reservation particulars and limits (1 to 12 guests per online request)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    number_of_guests = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    special_requests = models.TextField(blank=True, null=True)

    # Workflow status tracking and system timestamps
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booking_date', '-booking_time']

    def __str__(self):
        return f"Booking for {self.name} on {self.booking_date} at {self.booking_time}"