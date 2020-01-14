from django.contrib import admin

# Register your models here.
from .models import Product, Order, ProductSize, OrderDetail, CartItem, Category

admin.site.register(Order)
admin.site.register(ProductSize)
admin.site.register(OrderDetail)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Product)