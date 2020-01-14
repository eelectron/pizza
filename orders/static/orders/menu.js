document.addEventListener('DOMContentLoaded', function(){
	document.querySelectorAll(".addToCart").forEach(function(button){
		button.onclick = addToCart;
	});

	// hide pizza cost initially and show on select
	document.querySelectorAll(".products select").forEach(function(selectNode){
		selectNode.onchange = showCost;
	});

	//initially show only first pizza cost
	document.querySelectorAll(".product > .cost").forEach(function(pizzaCostNode){
		let spanNodes = pizzaCostNode.querySelectorAll("span");
		for(let i = 0; i < spanNodes.length; i++){
			spanNodes[i].style.display = "none";

			// show only first price
			if(i == 0){
				spanNodes[i].style.display = "block";
				pizzaCostNode.setAttribute("data-cost", spanNodes[i].dataset.cost);
				pizzaCostNode.parentElement.setAttribute("data-cost", spanNodes[i].dataset.cost);
				pizzaCostNode.parentElement.setAttribute("data-id", spanNodes[i].dataset.id);
				pizzaCostNode.parentElement.setAttribute("data-size", spanNodes[i].dataset.size);
			}
		}
	});

	// prevent submitting of empty cart
	document.querySelector("#myform").onsubmit = function(event){
		let cart = document.querySelector("#cart");
		if(cart.innerHTML.trim() == ""){
			return false;
		}
		else{
			return true;
		}
	}

	//total cost of saved cart item
	getTotalCostOfSavedItem();

	let cartNode = document.querySelector("#cart");
	cartNode.querySelectorAll(".removeFromCart").forEach(function(button){
		button.onclick = removeFromCart;
	});
});

// show price of pizza to user according to selected size  
function showCost(){
	const product = this.parentElement;
	const selectNode = product.querySelector("select");
	const pizzaCostNode = product.querySelector(".cost");

	product.querySelectorAll(".cost > span").forEach(function(spanNode){
		if(spanNode.dataset.id == selectNode.value){
			spanNode.style.display = "block";
			product.setAttribute("data-cost", spanNode.dataset.cost);
			product.setAttribute("data-id", spanNode.dataset.id);
			product.setAttribute("data-size", spanNode.dataset.size);
		}
		else{
			spanNode.style.display = "none";
		}
	});
}

// add pizza to cart
function addToCart(){
	let cart = document.querySelector("#cart");

	let id = this.parentElement.dataset.id;
	let item 	= this.parentElement.cloneNode(true);

	//remove unselected topping
	item.querySelectorAll(".topping").forEach(function(topping){
		if(topping.querySelector("input").checked == false){
			topping.remove();
		}

		//checkbox not required once item is in cart
		topping.querySelector("input").remove();
	});

	//remove drop down for size
	let selectNode 	= item.querySelector("select");
	if(selectNode != null){

		costNode = item.querySelector(".product > .cost");

		//div for size
		let divNode = document.createElement("div");
		divNode.setAttribute("class", "size");
		divNode.innerHTML = "size : " + item.dataset.size;
		item.replaceChild(divNode, selectNode);

		//div for cost
		let divCost = document.createElement("div");
		divCost.setAttribute("class", "cost");
		divCost.innerHTML = "$" + item.dataset.cost;
		item.replaceChild(divCost, costNode);
	}

	//add to cart
	cart.append(item);

	//save cart item in database
	saveCartItem(item);

	

	// change add to cart button to deleteFromCart
	let deleteFromCart = item.querySelector(".addToCart");
	deleteFromCart.innerHTML = "remove";
	deleteFromCart.setAttribute("class", "removeFromCart");

	// item should be deleted from cart on click
	deleteFromCart.onclick = removeFromCart;

	let totalCost = parseFloat(document.querySelector(".totalCost").innerHTML);

	//find item cost
	let cost = 0;
	cost += parseFloat(item.dataset.cost);

	item.querySelectorAll(".topping").forEach(function(costTag){
		cost += parseFloat(costTag.dataset.cost);
	});

	totalCost = totalCost + cost;
	totalCost = totalCost.toFixed(2);
	//display total cost
	document.querySelector(".totalCost").innerHTML = totalCost;
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

	cost += parseFloat(productTag.dataset.cost);

	productTag.querySelectorAll(".topping").forEach(function(toppingNode){
		cost += parseFloat(toppingNode.dataset.cost);
	});



	totalCost.innerHTML = (parseFloat(totalCost.innerHTML) - cost).toFixed(2);

	//remove this product from database also
	removeFromCartDatabase(productTag);

	//remove this item
	productTag.remove();
}

/* save cart item
// input : div tag
This function is called for every product which is added to cart .
*/
function saveCartItem(item){
	// get product id
	product = {};
	let id 	= item.dataset.id;

	product["id"] = id;

	// add toppings id if product is pizza
	subProductIds = [];
	item.querySelectorAll(".topping").forEach(function(subProduct){
		subProductIds.push(subProduct.dataset.id);
	});

	product["toppingIds"] = subProductIds;
	
	// save this item to database
	const request = new XMLHttpRequest();
	request.open("POST", "/saveCartItem/");
	request.onload = function(){
		let cartItemId = request.responseText;
		item.setAttribute("data-cartItemId", cartItemId);
	}

	let data = new FormData();
	data.append("product", JSON.stringify(product));

	// prevent cross site request forgery in ajax call
	request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	request.send(data);
}

//Remove this product cart in database
function removeFromCartDatabase(item){
	cartItem = {};
	cartItem["id"] = item.dataset.cartitemid;
	
	// save this item to database
	const request = new XMLHttpRequest();
	request.open("POST", "/removeCartItem/");
	request.onload = function(){

	}

	let data = new FormData();
	data.append("cartItem", JSON.stringify(cartItem));

	// prevent cross site request forgery in ajax call
	request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	request.send(data);
}

//total cost of saved cart item 
function getTotalCostOfSavedItem(){
	let cart = document.querySelector("#cart");
	let totalCostNode = document.querySelector(".totalCost");
	let totalCost = 0;

	cart.querySelectorAll("[data-cost]").forEach(function(costTag){
		totalCost += parseFloat(costTag.dataset.cost);
	});

	totalCost = totalCost.toFixed(2);	// 12.79898 ---> 12.80
	totalCostNode.innerHTML = totalCost;
}