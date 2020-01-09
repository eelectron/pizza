from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
#from django.views.decorators.csrf import csrf_protect

from .models import Pizza, Topping, Order, ToppingOrder, OrderDetail

import json

# Create your views here.
def index(request):
    return render(request, "orders/index.html")

def register(request):
	username 	= request.POST["username"]
	fn 			= request.POST["fname"]
	ln 			= request.POST["lname"]
	email 		= request.POST["email"]
	password	= request.POST["password"]

	user = User.objects.create_user(username=username, first_name=fn, last_name=ln, email=email, password=password)
	user.save()
	return HttpResponseRedirect(reverse("login"))
	#return HttpResponse("register")

def login_view(request):
	if request.method == 'GET':
		return render(request, "orders/login.html")

	# for post request
	try:
		username 	= request.POST["username"]
		password 	= request.POST["password"]
		user 		= authenticate(request, username=username, password=password)
	except:
		user 		= None

	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse("menu"))
	else:
		context = {"message": "Invalid credentials."}
		return render(request, "orders/login.html", context)

def menu(request):
	pizzas 		= Pizza.objects.all()
	toppings 	= Topping.objects.all()
 
	context = {
		"pizzas": pizzas,
		"toppings": toppings
	}
	return render(request, "orders/menu.html", context)


def logout_view(request):
	logout(request)
	return render(request, "orders/login.html", {"message": "Logged out"})


def buy(request):
	# insert order in database
	if request.method == "POST":
		products = json.loads(request.POST["products"])

		# total cost
		totalCost = int(request.POST["totalCost"])
		'''
		for product in products:
			pizzaId = int(product["pizzaid"])
			pizza 	= Pizza.objects.get(id=pizzaId)
			totalCost += pizza.price
			for toppingid in product["toppingids"]:
				topping 	= Topping.objects.get(id=int(toppingid))
				totalCost 	+= topping.price
		'''
		# insert order in Order table
		user = User.objects.get(username=request.user)
		order = Order(customer=user, cost=totalCost)
		order.save()

		for product in products:
			pizzaId = int(product["pizzaid"])
			pizza 	= Pizza.objects.get(id=pizzaId)
			od = OrderDetail(orderId=order, product=pizza)
			od.save()

			for toppingid in product["toppingids"]:
				topping = Topping.objects.get(id=int(toppingid))
				to = ToppingOrder(orderDetailId=od, toppingName=topping)
				to.save()
		print("Order placed!")
	return render(request, "orders/orderConfirmation.html", {"message": "Order placed, Thank You !"})


def orderConfirmation(request):
	pass