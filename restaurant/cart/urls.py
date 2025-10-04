# Define the urls for menu app
#  import path 
from django.urls import path

# Import views from the app
from . import views

app_name = 'cart'

# Define the url patterns
urlpatterns = [
    path('add/<int:dish_id>', views.add_to_cart, name='add_to_cart'),
]