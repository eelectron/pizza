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
}

// buy everything in cart
function buy(){
	
}