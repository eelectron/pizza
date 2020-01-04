from django.contrib import admin

# Register your models here.
from .models import Pizza, PizzaCost, Topping, Order

admin.site.register(Pizza)
admin.site.register(PizzaCost)
admin.site.register(Topping)
admin.site.register(Order)