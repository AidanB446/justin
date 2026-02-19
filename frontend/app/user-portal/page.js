'use client'

import styles from "./page.module.css";

export default function UserPortal() {
	
	// on the other side it should say edit existing account
	// where he can re assign tokens and paper trading boolean
	// also user deletion

	async function createNewUser() {
		const token = sessionStorage.getItem("token");
		// watch for error not sure if needs to be in a use effect	

		const username = document.getElementById("username");
		const api_key = document.getElementById("api_key");
		const api_secret = document.getElementById("api_secret");
		const paper_trading = document.getElementById("paper_trading");
		
		const url = "http://localhost:8000/usermod/create_account";
		
		const requestData = {
			"name": username.value,	
			"api_key": api_key.value,
			"api_secret": api_secret.value,
			"paper_trading": paper_trading.checked
		}

		const request = await fetch(url, {
			method: "POST",
			headers : {
				"Content-Type": "application/json",
				"Authorization": token
			},
			body: JSON.stringify(requestData),
		});
		
		switch (request.status) {
			case 200 :
				username.value = "";	
				api_key.value = "";	
				api_secret.value = "";	
				api_secret.value = "";	
				paper_trading.checked = false;
				document.getElementById("debugText").innerHTML = "User Created Successfully";
				document.getElementById("debugText").style.color = "blue";
				break;	

			case 401 :
				alert("bad auth please sign in again");
				window.location.href = "/";
				break;
				
			default :
				alert("site error please contact developer with details on encountering this message");
				break;

		}

	}

	return (
		<div>
			<input type="text" placeholder="Name" id="username" /><br/>	
			<input type="text" placeholder="Api Key" id="api_key"/><br/>						
			<input type="text" placeholder="Api Secret" id="api_secret"/><br/>						
			<label>
				<input type="checkbox" id="paper_trading" />
				Paper Trading
			</label>
			<br/>		
			<br/>		
			<button onClick={createNewUser}>Create User</button>
			<br/>		
			<br/>		
			<p id="debugText" ></p>
		</div>
	);
}

