"use client";

import styles from "./user.module.css";
import { useState, useRef } from "react";

export default function User(props) {
	const positionData = useRef(null);
	const stockSymbolInput = useRef(null);
	
	const buying_power_output = useRef(null);
	const cash_output = useRef(null);

	const [toggle, setToggle] = useState(true);

	function toggleSwitch() {
		setToggle(!toggle);
	}

	async function submitEdit() {
		const inputs = document.querySelectorAll("#editDiv > input");

		let bodyData = {};
		bodyData["name"] = props.username;
		for (const input of inputs) {
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

		for (const input of inputs) {
			if (input.type === "checkbox") {
				input.checked = false;
				continue;
			}
			input.value = "";
		}

		console.log(bodyData);

		const url = "http://localhost:8000/usermod/modify_account";
		console.log(props.token);
		const request = await fetch(url, {
			method: "POST",
			headers: {
				Authorization: props.token,
				"Content-Type": "application/json",
			},
			body: JSON.stringify(bodyData),
		});

		switch (request.status) {
			case 400:
				for (const input of inputs) {
					if (input.type === "checkbox") {
						input.checked = false;
						continue;
					}
					input.value = "";
				}
				alert("Please fill out all fields");
				break;

			case 200:
				window.location.reload();
				break;

			case 401:
				alert("Auth is no longer valid, please login");
				window.location.href = "/";

			default:
				break;
		}
	}

	async function deleteUser() {
		const request = await fetch(
			"http://localhost:8000/usermod/delete_account",
			{
				method: "POST",
				headers: {
					Authorization: props.token,
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ name: props.username }),
			},
		);

		switch (request.status) {
			case 200:
				window.location.reload();
				break;

			case 400:
				alert("Please fill out all forms of the field");
				break;
			case 401:
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

	async function getStockPos() {
		
		if (!stockSymbolInput) {
			alert("dom never rendered with the stockSymbolInput");
			return;	
		}
		
		const symbol = stockSymbolInput.current.value;

		const request = await fetch(
			"http://localhost:8000/get-stock-position",
			{
				method: "POST",
				headers: {
					Authorization: props.token,
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ name: props.username, symbol: symbol }),
			},
		);

		switch (request.status) {
			case 401:
				alert("Please login again");
				window.location.href = "/";
				return;

			case 400:
				const data = await request.json();
				console.log(data["error"]);
				alert(
					"Error retrieving stock position, please confirm you user keys, make sure all forms and filled correctly and try again.",
				);
				return;

			default:
				break;
		}

		const response = await request.json();

		if (positionData) {
			positionData.current.innerHTML = Object.entries(response)
				.map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(" ") : v}`)
				.join("<br>");
		}
	}


	async function getBuyingPower() {
		buying_power_output.current.innerHTML = "Please stand by";	

		const token = sessionStorage.getItem("token") || null;	
			
		if (token === null) {
			alert("Please log in again, bad auth");
			buying_power_output.current.innerHTML = "";	
			window.location.href = "/";
			return;
		}
		
		const url = "http://localhost:8000/get-buying-power";
		const bodyData = {"users": [props.username]}	
		
		const request = await fetch(url, {
			method: "POST",
			headers: {
				"Authorization": token,
				"Content-Type": "application/json",
			},
			body: JSON.stringify(bodyData)
		});
		
		switch (request.status) {
		
			case 401 :
				alert("Please sign in again auth failed");
				window.location.href = "/";	
				return;

			case 200 :
				const data = await request.json();
				const userObj = data[props.username]
				
				try {
					buying_power_output.current.innerHTML = userObj["buying_power"]	
					cash_output.current.innerHTML = userObj["cash"];	
				} catch (error) {
					buying_power_output.current.innerHTML = "Error Getting Value, verify user keys";	
				}
				break;

			default :
				buying_power_output.current.innerHTML = "";	
				alert("Unhandled error, please contact developer with details on encountering this message.");	
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
					<button onClick={getBuyingPower}>Get Buying Power</button>
					<p ref={buying_power_output}></p>
					<p ref={cash_output}></p>
					<br />
					<br />
					<div className={styles.getStockPosition}>
						<h3>Get Stock Position</h3>
						<input
							ref={stockSymbolInput}
							id="stockSymbol"
							type="text"
							placeholder="Enter Stock Symbol"
						/>
						<button onClick={getStockPos}>Get Position</button>
						<br />
						<br />
						<p ref={positionData}></p>
					</div>
				</div>
			</details>
		);
	} else {
		return (
			<details className={styles.container}>
				<summary className={styles.header}>{props.username}</summary>
				<div id="editDiv" className={styles.content}>
					<h3>Old Data</h3>
					<span>Previous API_KEY: {props.api_key}</span>
					<br />
					<span>Previous API_SECRET: {props.api_secret}</span>
					<br />
					<br />
					<input name="api_key" placeholder="Enter New Api Key" />
					<br />
					<input
						name="api_secret"
						placeholder="Enter New Api Secret"
					/>
					<br />
					<label>Paper Trading</label>
					<input type="checkbox" name="paper_trading" />
					<br />
					<br />
					<button onClick={submitEdit}>Submit Edit</button>
					<br />
					<br />
					<br />
					<button onClick={toggleSwitch}>Done Editing</button>
				</div>
			</details>
		);
	}
}
