from django.db import models

# import CustomerProfile and MenuItem models
from customers.models import CustomerProfile
from menu.models import MenuItem

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(MenuItem, through='Order_MenuItem')
    created_at = models.DateTimeField(auto_now_add=True)
    # class -> to define the options -> enums
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSED ='PROCESSED','Processed'
        DELIVERED = 'DELIVERED','Delivered' # Status.DELIVERED
        CANCELLED = 'CANCELLED', 'Cancelled'

    status = models.CharField(max_length=30,
                              choices= Status.choices,
                              default=Status.PENDING)
    
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

class Order_MenuItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products' )
    product_id = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name= 'menu_products' )
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.quantity * self.price