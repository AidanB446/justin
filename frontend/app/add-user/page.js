'use client'

import styles from "./page.module.css";


export default function AddUser() {
	

	async function createNewUser() {
		const token = sessionStorage.getItem("token");
		// watch for error not sure if needs to be in a use effect	


		const username = document.getElementById("username");
		const api_key = document.getElementById("api_key");
		const api_secret = document.getElementById("api_secret");
		const paper_tradingBool = document.getElementById("paper_trading").checked;
		
		const url = "http://localhost:8000/usermod/create_account";
		
		const requestData = {
			"name": username,	
			"api_key": api_key,
			"api_secret": api_secret,
			"paper_trading": paper_tradingBool

		}

		const request = await fetch(url, {
			method: "POST",
			headers : {
				"Content-Type": "application/json",
				"Authorization": token
			},
			body: JSON.stringify(requestData),
		});
	
		if (!request.status === 200) {

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

			<button onClick={createNewUser}>Create User</button>
		</div>
	);
}



