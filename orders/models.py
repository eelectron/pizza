from django.db import models
from django.contrib.auth.models import User

class ProductSize(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name        = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    price       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    size        = models.ForeignKey(ProductSize, on_delete=models.CASCADE, blank=True, null=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    parentProduct = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.description}, {self.size} size , ${self.price}, {self.category}"


class Order(models.Model):
    customer    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    cost        = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.customer} , Total cost = {self.cost}"


class OrderDetail(models.Model):
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parent  = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.orderId}, {self.product}"

'''
Persist items added to cart .
'''
class CartItem(models.Model):
    customer    = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    parent      = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.customer}, {self.product}"
