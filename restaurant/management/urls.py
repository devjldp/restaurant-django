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
    path('dashboard/dishes/', views.management_select_all_dishes, name='list_dishes'),
    path('dashboard/add_dish/', views.management_add_dish, name='add_dish'),
    path('dashboard/delete_dish/<int:dish_id>/', views.management_delete_dish, name = 'delete_dish'),
    path('dashboard/update_dish/<int:dish_id>/',views.management_update_dish, name='update_dish')
    
]