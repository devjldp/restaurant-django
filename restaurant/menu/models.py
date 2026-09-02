from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Category(models.Model):
    """
        Represents a category used to organise menu items.

        Categories allow customers to browse the restaurant menu
        in a clear and structured way. For example, a category may
        represent Starters, Main Courses, Desserts or Drinks.
    """
    name = models.CharField(max_length=150, unique=True)
    # Allows administrators to temporarily hide a category without permanently deleting its associated data.
    display_order = models.PositiveIntegerField(default=0,  help_text="Display order on the menu (e.g. 1 for Starters, 2 for Mains)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["display_order","name"]
    def __str__(self):
        return self.name

    
class Ingredient(models.Model):
    """
        Represents an ingredient that can be associated with
        one or more menu items.

        Ingredients are stored separately so that the same ingredient
        can be reused across multiple dishes without duplicating data.
        This creates a many-to-many relationship with MenuItem.
    """

    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    """
        Represents an individual dish or product available on
        the restaurant menu.

        Menu items contain the information presented to customers,
        including the name, description, price, nutritional information,
        dietary information, availability and associated ingredients.
    """
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    calories = models.PositiveIntegerField(default=0)

    # Relationship 1 - M: 1 Category - Many MenuItem
    # SET_NULL preserves the MenuItem if its category is removed.
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='menu_items')

    # Relationship Many to Many: Many Ingredient - Many MenuItem
    ingredients = models.ManyToManyField(Ingredient, related_name='menu_items', blank=True)

    # Dietary information used to help customers identify suitable menu choices.
    is_vegetarian = models.BooleanField(default = False)
    is_vegan = models.BooleanField(default = False)

    # Controls whether the item is currently visible/available for ordering.
    is_available = models.BooleanField(default = True)
    is_available_delivery = models.BooleanField(default = True)

    # image
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name