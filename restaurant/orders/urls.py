# Define the urls for orders app
#  import path 
from django.urls import path

# Import views from the app
from . import views

app_name = 'orders'

# Define the url patterns
urlpatterns = [
    path('', views.create_order, name='order'),
    path('pay/<int:order_id>/', views.pay_order, name='pay_order'),
    path('success/<int:order_id>/', views.payment_succes, name= 'payment_success'),
    path('cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel')

]