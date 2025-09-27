# import class forms
from django import forms
from .models import MenuItem, Ingredient, Category

# Form to add a new dish
class MenuItemForm(forms.ModelForm):
    
    # relationship one to many -> automatically managed by django creating a select element.
    # relationship many to many -> automatically managed by django using checkboxes.
    
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'calories', 'category', 'ingredients', 'is_vegetarian',
                  'is_vegan', 'is_available', 'is_available_delivery']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
            'price': forms.NumberInput(attrs={'step':'0.01'}),
            'ingredients':forms.CheckboxSelectMultiple(),
        }
        