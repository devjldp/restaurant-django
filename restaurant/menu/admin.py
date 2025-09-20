from django.contrib import admin

# import models
from .models import MenuItem, Ingredient, Category
# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Ingredient)
admin.site.register(Category)

