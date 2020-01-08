document.addEventListener('DOMContentLoaded', function(){
	document.querySelectorAll(".addToCart").forEach(function(button){
		button.onclick = addToCart;
	});

	// on buy
	document.querySelector("#buy").onclick = buy();
});


// add pizza to cart
function addToCart(){
	let cart = document.querySelector("#cart");

	let item = this.parentElement.cloneNode(true);
	cart.append(item);

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
	
}