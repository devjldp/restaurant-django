# Define the urls for menu app
#  import path 
from django.urls import path

# Import views from the app
from . import views

app_name = 'menu'

# Define the url patterns
urlpatterns = [
    path('', views.select_all_menu, name='menu_list')
    # define more paths - urls
]