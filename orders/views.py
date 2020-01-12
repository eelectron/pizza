from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
#from django.views.decorators.csrf import csrf_protect

from .models import Pizza, Topping, Order, ToppingOrder, OrderDetail, CartItem, CartItemTopping, BasePizza

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
	# display menu
	basePizzas 	= BasePizza.objects.all()
	toppings 	= Topping.objects.all()

	#get all corresponding pizza or every base pizza
	pizzas = []
	for bp in basePizzas:
		pizza = {}
		pizza["basePizza"] = bp
		pizza["pizzas"] = bp.pizza_set.all() 
		pizzas.append(pizza)

	# display saved cart item
	user 		= User.objects.get(username=request.user)
	cartItems 	= CartItem.objects.filter(customer=user)
	
	# get all toppings
	items = []
	for item in cartItems:
		product = {}
		product["cartItem"] = item
		print(item)
		product["cartItemToppings"] = CartItemTopping.objects.filter(cartItem=item.id)
		items.append(product)

	context = {
		"basePizzas": basePizzas,
		"pizzas" : pizzas,
		"toppings": toppings,
		"cartItems" : items
	}
	return render(request, "orders/menu.html", context)


def logout_view(request):
	logout(request)
	return render(request, "orders/login.html", {"message": "Logged out"})


def buy(request):
	# insert order in Order table
	user 		= User.objects.get(username=request.user)
	cartItems 	= CartItem.objects.filter(customer=user)
	
	# total cost of cart items
	totalCost = 0

	# get all product from cart
	products = []
	for item in cartItems:
		product = {}
		product["pizzaid"] = item.product.id
		cartItemToppings = CartItemTopping.objects.filter(cartItem=item.id)

		totalCost += item.product.price
		product["toppings"] = []
		for cit in cartItemToppings:
			totalCost += cit.topping.price
			product["toppings"].append(cit.topping)
		products.append(product)

	order = Order(customer=user, cost=totalCost)
	order.save()

	# add to order
	for product in products:
		pizzaId = int(product["pizzaid"])
		pizza 	= Pizza.objects.get(id=pizzaId)
		od = OrderDetail(orderId=order, product=pizza)
		od.save()

		for topping in product["toppings"]:
			to = ToppingOrder(orderDetailId=od, toppingName=topping)
			to.save()

	# delete cart items because customer has purchased it
	cartItems.delete()
	context = {
		"message": "Order placed, Thank You !",
		"orderNo": "Your order number is " + str(order.id)
	}
	return render(request, "orders/success.html", context)


'''
Display all items of cart for order confirmation .
'''
def orderConfirmation(request):
	if request.method == "POST":
		user 		= User.objects.get(username=request.user)
		cartItems 	= CartItem.objects.filter(customer=user)
		
		# total cost of cart items
		totalCost = 0

		# get all toppings
		items = []
		for item in cartItems:
			product = {}
			product["cartItem"] = item
			cartItemToppings = CartItemTopping.objects.filter(cartItem=item.id)
			product["cartItemToppings"] = cartItemToppings
			items.append(product)

			totalCost += item.product.price
			for cit in cartItemToppings:
				totalCost += cit.topping.price


		context = {
			"cartItems" : items,
			"totalCost" : totalCost
		}
		return render(request, "orders/orderConfirmation.html",context)

'''
Save items of cart .
input : id of pizza
'''
def saveCartItem(request):
	if request.method == "POST":
		product = json.loads(request.POST["product"])
		id 		= int(product["id"])
		pizza 	= Pizza.objects.get(id=id)
		user 	= User.objects.get(username=request.user)

		cartItem = CartItem(customer=user, product=pizza)
		cartItem.save()

		# save if any topping is associated with the pizza
		if "toppingIds" in product:
			for toppingId in product["toppingIds"]:
				topping = Topping.objects.get(id=int(toppingId))
				toppingItem = CartItemTopping(cartItem=cartItem, topping=topping)
				toppingItem.save()
	return HttpResponse(f"{cartItem.id}")


def removeCartItem(request):
	if request.method == "POST":
		cartItem = json.loads(request.POST["cartItem"])
		id 		= int(cartItem["id"])

		cartItem = CartItem.objects.get(id=id)
		cartItem.delete()
	return HttpResponse(f"cartItemId {id} is removed")