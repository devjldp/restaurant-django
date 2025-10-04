from django.db import models
from django.conf import settings # Reference the model user
from django.contrib.auth.models import User # Signal

# Create your models here.
class CustomerProfile(models.Model):
    # 1 to 1 relationship
    user = models.OneToOneField( #username
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'profile' # allows to access to profile from the user: request.user.profile
        )
    
    # Fields for delivery
    first_name =models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    post_code = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for: {self.user.username}"

