from django.contrib import admin

# Register your models here.
from .models import BasePizza, Pizza, Topping, Order, PizzaSize, OrderDetail, ToppingOrder, CartItem, CartItemTopping

admin.site.register(Pizza)
#admin.site.register(PizzaCost)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(PizzaSize)
admin.site.register(OrderDetail)
admin.site.register(BasePizza)
admin.site.register(ToppingOrder)
admin.site.register(CartItem)
admin.site.register(CartItemTopping)