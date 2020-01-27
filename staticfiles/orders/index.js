document.addEventListener("DOMContentLoaded", function(){
	let registerButton = document.querySelector("[type=submit]").disabled = true;
	document.querySelector(".username > input").onkeyup = isUsernameAvailable;
});

function isUsernameAvailable(){
	let parent = this.parentElement;
	let feedback = parent.querySelector("span");
	let username = this.value;
	username = username.trim();
	let registerButton = document.querySelector("[type=submit]");

	const request = new XMLHttpRequest();
	request.open("POST", "/isUsernameAvailable/");
	request.onload = function(){
		const data = request.responseText;
		//console.log(data);
		if(data == "yes"){
			feedback.style.border = "2px solid green";
			feedback.innerHTML = "username available :)";
			registerButton.disabled = false;
		}
		else{
			feedback.style.border = "2px solid red";
			feedback.innerHTML = "username not available :(";
			registerButton.disabled = true;	
		}
	}

	const data = new FormData();
	data.append("username", username);

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