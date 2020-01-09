document.addEventListener('DOMContentLoaded', function(){
	document.querySelectorAll(".addToCart").forEach(function(button){
		button.onclick = addToCart;
	});

	// on buy
	document.querySelector("#buy").onclick = buy;
});


// add pizza to cart
function addToCart(){
	let cart = document.querySelector("#cart");

	let item = this.parentElement.cloneNode(true);

	//remove unselected topping
	item.querySelectorAll(".topping").forEach(function(topping){
		if(topping.querySelector("input").checked == false){
			topping.remove();
		}
	});

	cart.append(item);

	// change add to cart button to deleteFromCart
	let deleteFromCart = item.querySelector(".addToCart");
	deleteFromCart.innerHTML = "remove";

	// item should be deleted from cart on click
	deleteFromCart.onclick = removeFromCart;

	let totalCost = parseFloat(document.querySelector(".totalCost").innerHTML);

	//calculate total cost
	let pizzaCost = parseFloat(item.querySelector("div.pizzaCost span").innerHTML);

	//find topping cost
	let toppingCost = 0;
	item.querySelectorAll("div.topping").forEach(function(topping){
		// is checked
		if(topping.querySelector("input").checked == true){
			toppingCost += parseFloat(topping.querySelector("div.toppingCost span").innerHTML);
		}
	});

	totalCost = totalCost + pizzaCost + toppingCost;

	//display total cost
	document.querySelector(".totalCost").innerHTML = totalCost;
}

// buy everything in cart
function buy(){
	products = [];
	let cart = document.querySelector("#cart");
	if(cart.hasChildNodes() == false){
		return;
	}

	cart.querySelectorAll(".pizza").forEach(function(pizza){
		pizzaWithTopping = {};
		pizzaWithTopping["pizzaid"] = pizza.dataset.pizzaid;

		// get toppings
		toppingIds = [];
		pizza.querySelectorAll(".topping").forEach(function(topping){
			if(topping.querySelector("input").checked == true){
				toppingIds.push(topping.dataset.toppingid);
			}
		});

		pizzaWithTopping["toppingids"] = toppingIds;

		//add to products
		products.push(pizzaWithTopping);

		console.log(products);

		
	});

	// send to server
	const request = new XMLHttpRequest();
	request.open("POST", '/buy/');
	request.onload = function(){
		// redirect to buy detail page
		location.replace(location.origin + "/orderConfirmation/");
	}

	const data = new FormData();
	jsonProducts = JSON.stringify(products);
	data.append('products',jsonProducts);
	data.append('totalCost', document.querySelector(".totalCost").innerHTML)

	// prevent cross site request forgery in ajax call
	request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	request.send(data);
}


// Get csrftoken value from cookie
function getCookie(key){
	let value = null;
	if(document.cookie && document.cookie !== ''){
		let cookies = document.cookie.split(';');
		for(let i = 0; i < cookies.length; i++){
			let cookie = cookies[i].trim();
			if(cookie.substring(0, key.length) == key){
				value = decodeURIComponent(cookie.substring(key.length + 1));
				break;
			}
		}
	}
	return value;
}

// remove an item from cart and reduce from totalCost
function removeFromCart(){
	let cost = 0;
	let totalCost = document.querySelector(".totalCost");
	let productTag = this.parentElement;

	productTag.querySelectorAll(".cost").forEach(function(costTag){
		cost += parseFloat(costTag.innerHTML);
	});
	totalCost.innerHTML = parseFloat(totalCost.innerHTML) - cost;

	//remove this item
	this.parentElement.remove();
}