# Define the urls for menu app
#  import path 
from django.urls import path

# Import views from the app
from . import views

app_name = 'cart'

# Define the url patterns
urlpatterns = [
    path('', views.display_cart, name='cart'),
    path('add/<int:dish_id>', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:dish_id>', views.increase_dish, name='increase_dish'),
    path('decrease/<int:dish_id>', views.decrease_dish, name = 'decrease_dish'),
    path('remove/<int:dish_id>', views.remove_dish, name='remove_dish'),
    path('clear/', views.clear_cart, name='clear_cart'),
]