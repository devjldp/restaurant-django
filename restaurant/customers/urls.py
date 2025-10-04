# Define the urls for menu app
#  import path 
from django.urls import path

# Import views from the app
from . import views

app_name = 'customers'

# Define the url patterns
urlpatterns = [
    path('', views.create_profile, name='create_profile'),
    # define more paths - urls
   
]