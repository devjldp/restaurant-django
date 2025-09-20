import os
import json
import django

# Set up django configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from menu.models import Category, Ingredient, MenuItem

json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'menu.json')

with open(json_path, 'r', encoding='utf-8') as file:
    menu_data = json.load(file)

# print(len(menu_data))

categories = []
ingredients = []
for menu_item in menu_data:
    if menu_item['category'] not in categories:
        categories.append(menu_item['category'])
    for ingredient in menu_item['ingredients']:
        if ingredient not in ingredients:
            ingredients.append(ingredient)

# print(categories)
# print(ingredients)

# Populate table category
# for category in categories:
#     category_object, created = Category.objects.get_or_create(name = category)

#     if created:
#         print(f"{category} created susscess")
#     else:
#         print(f"{category} created unsusscess")

# Populate table ingredients.
# for ingredient in ingredients:
#     ingredient_object, created = Ingredient.objects.get_or_create(name = ingredient)

#     if created:
#         print(f"{ingredient} created susscess")
#     else:
#         print(f"{ingredient} created unsusscess")



# Columns: name, description, price, calories, is_vegetarian, is_vegan, is_available, is_available_Delivery, image, category_id

for dish in menu_data:
    # # get the value for the key category
    category_name = dish.get('category')
    # # get the object category from the database - table category
    category_obj = Category.objects.get(name=category_name) 
    # # Insert the menu item in the table  
    menu_item_object, created = MenuItem.objects.get_or_create(
        name = dish.get('name'),
        description = dish.get('description'),
        price = dish.get('price'),
        calories = dish.get('kilocalories'),
        category = category_obj, # Relate foreign key
        is_vegetarian = dish.get('is_vegetarian'),
        is_vegan = dish.get('is_vegan'),
        is_available = dish.get('is_available'),
        is_available_delivery = dish.get('is_available_delivery'),
        image = dish.get('image')
    )
    
    # #Relation Many to Many

    # # Check if ingredients exists and list of ingridients is not empty.
    if 'ingredients' in dish and dish['ingredients']: 
        # Iterate over the list
        for ingredient in dish['ingredients']:
            # Get the ingredient form the database - table: Ingredient
            ingredient_obj = Ingredient.objects.get(name=ingredient)
            # Create the relationship many to many: menu_item_object is the object we created
            menu_item_object.ingredients.add(ingredient_obj) # Add the object
    # print(dish.get('kilocalories'))
    # print(type(dish.get('kilocalories')))
  

