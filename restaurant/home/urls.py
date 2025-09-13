# We are going to define the specific url for home app
#  import path 
from django.urls import path

# Import views from the app
from . import views

app_name = 'home'

# Define the url patterns
urlpatterns = [
    path('', views.index, name='index')
    # '' -> route string
    # views.index -> view function that handles the request
    # name='index -> unique name for the route


]