# Define the urls for menu app
#  import path 
from django.urls import path

# Import views from the app
from . import views

app_name = 'management'

# Define the url patterns
urlpatterns = [
    path('dashboard/', views.management_home, name='home'),
    # define more paths - urls
    
]