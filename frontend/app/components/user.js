"use client";

import styles from "./user.module.css";
import { useState} from "react";

export default function User(props) {
		
	const [toggle, setToggle] = useState(true);
		
	function toggleSwitch() {
		setToggle(!toggle);
	}		
	
	async function submitEdit() {
		const inputs = document.querySelectorAll("#editDiv > input");	
	
		let bodyData ={};
		bodyData["name"] = props.username; 	
		for (const input of inputs)	{
			if (input.type === "checkbox") {
				bodyData["paper_trading"] = Number(input.checked); 	
				continue;
			}
			
			if (input.value === "") {
				alert("Please Fill Out All Fields");
				return;	
			}

			bodyData[input.name] = input.value; 	
		}
	
		for (const input of inputs)	{
			if (input.type === "checkbox") {
				input.checked = false;	
				continue;
			}
			input.value = "";
		}
		
		console.log(bodyData);

		const url = "http://localhost:8000/usermod/modify_account";		
		const request = await fetch(url, {
			method: "POST",
			headers : {
				"Authorization": props.token,
				"Content-Type": "application/json"
			},
			body: JSON.stringify(bodyData),
		});	
		
		switch (request.status) {
			case 400: 
				for (const input of inputs)	{
					if (input.type === "checkbox") {
						input.checked = false;	
						continue;
					}
					input.value = "";
				}
				alert("Please fill out all fields");
				break;

			case 200 :
				window.location.reload()


			default :
				break;
			
		}

	}
	
	async function deleteUser() {
		const token = sessionStorage.getItem("token");

		if (token === null) {
			alert("Please sign in again.");
			window.location.href = "/";
		}
		
		const request = await fetch("http://localhost:8000/usermod/delete_account", {
			method: "POST",
			headers: {
				"Authorization": token,
				"Content-Type": "application/json"
			},
			body : JSON.stringify({"name": props.username})	
		});

		switch (request.status) {
			case 200:
				window.location.reload();
				break;

			case 400:
				alert("Please fill out all forms of the field");
				break;
			case 401 :
				alert("Please log in again");
				window.location.href = "/";
				break;
			
			default:
				alert(
					"site error please contact developer with details on encountering this message",
				);
				break;
		}

	}

	if (toggle) {
		return (
			<details className={styles.container}>
				<summary className={styles.header}>{props.username}</summary>
				<div className={styles.content}>
					<p>api key: {props.api_key}</p>
					<p>api secret: {props.api_secret}</p>
					<p>paper trading: {props.paper_trading}</p>
					<button onClick={toggleSwitch}>Edit Values</button>	
					<button onClick={deleteUser}>Delete User</button>	
				</div>
			</details>
		);
	} else {

		return (
			<details className={styles.container}>

				<summary className={styles.header}>{props.username}</summary>
				<div id="editDiv" className={styles.content}>
					<input name="api_key" placeholder="Enter Api Key" /><br/>
					<input name="api_secret" placeholder="Enter Api Secret" /><br/>
					<label>
						Paper Trading 
					</label>
					<input type="checkbox" name="paper_trading" />
					<br/>
					<br/>
					<button onClick={submitEdit}>Submit Edit</button>
					<br/>
					<br/>
					<br/>
					<button onClick={toggleSwitch}>Done Editing</button>	
				</div>
			</details>
		)	
	} 
}
