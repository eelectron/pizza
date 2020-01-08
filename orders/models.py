from django.db import models
from django.contrib.auth.models import User

class Topping(models.Model):
    name    = models.CharField(max_length=64)
    price   = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # pizza = models.ForeignKey(Pizza, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f"{self.id} - {self.name} ${self.price} dollars"


class PizzaSize(models.Model):
    size = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} - {self.size}"


class Product(models.Model):
    name        = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    
    def __str__(self):
        return f"{self.name} - {self.description}"


# Create your models here.
# Pizza without size property
class BasePizza(Product):
    def __str__(self):
        return f"{self.id} - {self.name} , {self.description}"
    

class Pizza(Product):
    base    = models.ForeignKey(BasePizza, on_delete=models.CASCADE, default=None)
    size    = models.ForeignKey(PizzaSize, on_delete=models.CASCADE, blank=True, null=True)
    #topping = models.ManyToManyField(Topping, blank=True)
    price   = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.id} - {self.name} , {self.size} size , {self.description}, ${self.price}"

'''
class PizzaCost(models.Model):
    pizza   = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    #size    = models.ForeignKey(PizzaSize, on_delete=models.SET_NULL, null=True)
    price   = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.pizza} of ${self.price}"
'''

class Order(models.Model):
    customer    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    # pizza       = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="pizza")

    def __str__(self):
        return f"{self.customer} ordered {self.pizza}"


class OrderDetail(models.Model):
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.orderId}, {self.product}"


class ToppingOrder(models.Model):
    orderDetailId = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    toppingName = models.ForeignKey(Topping, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.orderDetailId} - {self.toppingName}"