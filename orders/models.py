from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pizza(models.Model):
	name 		= models.CharField(max_length=64)
	description = models.CharField(max_length=512)
	size 		= models.CharField(max_length=64) 
	# topping 	= models.ForeignKey(Topping, null=True)	

	def __str__(self):
		return f"{self.name} , {self.size} size , {self.description}"


class Topping(models.Model):
	name 	= models.CharField(max_length=64)
	price 	= models.DecimalField(max_digits=10, decimal_places=2, default=0)
	pizza   = models.ForeignKey(Pizza, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.id} - {self.name} ${self.price} dollars"



class PizzaCost(models.Model):
	pizza 	= models.ForeignKey(Pizza, on_delete=models.CASCADE)
	small	= models.DecimalField(max_digits=10, decimal_places=2, default=0)
	medium	= models.DecimalField(max_digits=10, decimal_places=2, default=0)
	large	= models.DecimalField(max_digits=10, decimal_places=2, default=0)

	def __str__(self):
		return f"small : ${self.small} dollars, medium : ${self.medium} dollars, large : ${self.large} dollars"


class Order(models.Model):
	customer	= models.ForeignKey(User, on_delete=models.CASCADE)
	pizza 		= models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="orders")

	def __str__(self):
		return f"{self.customer} ordered {self.pizza} with toppings as {self.topping1}, {self.topping2}"


