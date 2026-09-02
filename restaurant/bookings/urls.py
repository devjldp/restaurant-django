from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.create_booking, name='create_booking'),
    path('my-bookings/', views.user_bookings, name='user_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]