from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

    
class Ingredient(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    calories = models.IntegerField(default=0)

    # Relationship 1 - M: 1 Category - Many MenuItem
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True, related_name='menu_items')

    # Relationship Many to Many: Many Ingredient - Many MenuItem
    ingredients = models.ManyToManyField(Ingredient, related_name='menu_items')

    is_vegetarian = models.BooleanField(default = False)
    is_vegan = models.BooleanField(default = False)
    is_available = models.BooleanField(default = True)
    is_available_delivery = models.BooleanField(default = True)

    # image
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name