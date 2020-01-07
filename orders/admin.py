from django.contrib import admin

# Register your models here.
from .models import BasePizza, Pizza, PizzaCost, Topping, Order, PizzaSize, OrderDetail, ToppingOrder

admin.site.register(Pizza)
admin.site.register(PizzaCost)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(PizzaSize)
admin.site.register(OrderDetail)
admin.site.register(BasePizza)
admin.site.register(ToppingOrder)