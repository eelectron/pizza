from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core import mail
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.utils.html import strip_tags


#from django.views.decorators.csrf import csrf_protect

from .models import Product, Order, OrderDetail, CartItem, Category, ProductSize

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


def logout_view(request):
	logout(request)
	return render(request, "orders/login.html", {"message": "Logged out"})


'''
Display all hotel's menu
'''
def menu(request):
	# display menu
	toppingCategory = Category.objects.get(name="Topping")
	products 	= Product.objects.filter(parentProduct=None).exclude(category=toppingCategory)
	toppings 	= Product.objects.filter(category=toppingCategory)

	#get all corresponding pizza or every base pizza
	productList = []
	for product in products:
		p = {}
		p["basePizza"] = product
		p["pizzas"] = product.product_set.all() 
		productList.append(p)

	# display saved cart item
	user 		= User.objects.get(username=request.user)
	cartItems 	= CartItem.objects.filter(customer=user, parent=None)
	
	# get all toppings
	items = []
	for item in cartItems:
		product = {}
		product["cartItem"] = item
		product["cartItemToppings"] = item.cartitem_set.all()
		items.append(product)

	context = {
		"pizzas" : productList,
		"toppings": toppings,
		"cartItems" : items
	}
	return render(request, "orders/menu.html", context)


'''
Display all items of cart for order confirmation .
'''
def orderConfirmation(request):
	if request.method == "POST":
		user 		= User.objects.get(username=request.user)
		cartItems 	= CartItem.objects.filter(customer=user, parent=None)
		
		# total cost of cart items
		totalCost = 0

		# get all pizza with toppings
		items = []
		for item in cartItems:
			product = {}
			product["cartItem"] = item
			cartItemToppings = item.cartitem_set.all()
			product["cartItemToppings"] = cartItemToppings
			items.append(product)

			totalCost += item.product.price
			for cit in cartItemToppings:
				totalCost += cit.product.price


		context = {
			"cartItems" : items,
			"totalCost" : totalCost
		}
		return render(request, "orders/orderConfirmation.html",context)




def buy(request):
	# insert order in Order table
	user 		= User.objects.get(username=request.user)
	cartItems 	= CartItem.objects.filter(customer=user, parent=None)
	
	# total cost of cart items
	totalCost = 0

	# get all product from cart
	products = []
	emailItems = []
	for item in cartItems:
		product = {}
		product["pizzaid"] = item.product.id
		toppings = item.cartitem_set.all()

		emailItem = {}
		emailItem["cartItem"] = item
		emailItem["cartItemToppings"] = toppings
		emailItems.append(emailItem)

		totalCost += item.product.price
		product["toppings"] = []
		for cit in toppings:
			totalCost += cit.product.price
			product["toppings"].append(cit.product)
		products.append(product)

	order = Order(customer=user, cost=totalCost)
	order.save()

	# add to order
	for product in products:
		pizzaId = int(product["pizzaid"])
		pizza 	= Product.objects.get(id=pizzaId)
		od = OrderDetail(orderId=order, product=pizza)
		od.save()

		for topping in product["toppings"]:
			to = OrderDetail(orderId=order, product=topping, parent=od)
			to.save()

	
	context = {
		"cartItems": emailItems,
		"totalCost": totalCost
	}

	# send order num to email
	sendEmail(request, order.id, context)

	context["message"] = "Order placed, Thank You !"
	context["orderNo"] = "Your order number is " + str(order.id)
	context["emailId"] = user.email

	# delete cart items because customer has purchased it
	cartItems.delete()
	return render(request, "orders/success.html", context)



'''
Save items of cart .
input : id of pizza
'''
def saveCartItem(request):
	if request.method == "POST":
		product = json.loads(request.POST["product"])
		id 		= int(product["id"])
		pizza 	= Product.objects.get(id=id)
		user 	= User.objects.get(username=request.user)

		cartItem = CartItem(customer=user, product=pizza)
		cartItem.save()

		# save if any topping is associated with the pizza
		if "toppingIds" in product:
			for toppingId in product["toppingIds"]:
				topping = Product.objects.get(id=int(toppingId))
				toppingItem = CartItem(parent=cartItem, customer=user, product=topping)
				toppingItem.save()
	return HttpResponse(f"{cartItem.id}")


def removeCartItem(request):
	if request.method == "POST":
		cartItem = json.loads(request.POST["cartItem"])
		id 		= int(cartItem["id"])

		cartItem = CartItem.objects.get(id=id)
		cartItem.delete()
	return HttpResponse(f"cartItemId {id} is removed")

def sendEmail(request, orderId, context):
	subject = f"Pizza Order Number {orderId}"
	html_message = render_to_string("orders/emailTemplate.html", context)
	message = strip_tags(html_message)
	fm = "prashantexploring@gmail.com"
	toEmailId = User.objects.get(username=request.user)
	to = [toEmailId.email]
	msg = mail.send_mail(subject, message, fm, to, html_message=html_message)


def isUsernameAvailable(request):
	if request.method == "POST":
		try:
			user = User.objects.get(username=request.POST["username"])
		except User.DoesNotExist:
			return HttpResponse("yes")
		return HttpResponse("no")



# rest framework
from rest_framework import serializers, viewsets
from orders.serializers import ProductSerializer, CategorySerializer
from rest_framework import viewsets
from django.core import serializers

'''
@api_view(['GET'])
def getProducts(self, request):
		pList = Product.objects.all()
		serializer = ProductSerializer(pList, many=True)
		return Response(serializer.data)
'''
class ProductView(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


class CategoryView(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer