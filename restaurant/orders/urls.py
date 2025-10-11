# Define the urls for orders app
#  import path 
from django.urls import path

# Import views from the app
from . import views

app_name = 'orders'

# Define the url patterns
urlpatterns = [
    path('', views.create_order, name='order'),
]