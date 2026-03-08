"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

export default function Home() {
	const [users, setUsers] = useState([]);
	const [usernames, setUsernames] = useState(["please,", "wait"]);
	const [token, setToken] = useState("");

	useEffect(() => {
		const token = sessionStorage.getItem("token");

		if (token === null) {
			window.location.href = "/";
		}

		setToken(token);

		async function get_users() {
			const url = "http://localhost:8000/get-all-users";
			const request = await fetch(url, {
				method: "GET",
				headers: {
					Authorization: token,
				},
			});

			const response = await request.json();

			switch (request.status) {
				case 200:
					setUsers(response["users"]);
					const usernamesFound = [];

					for (let i = 0; i < response["users"].length; i++) {
						const newUsername = response["users"][i].name;
						usernamesFound.push(newUsername);
					}

					setUsernames(usernamesFound);
					break;

				case 401:
					alert("Auth no longer valid please sign in again");
					window.location.href = "/";
					break;

				default:
					alert(
						"Internal applciation error please contact developer with details on how you encountered this message.",
					);
			}
		}

		get_users();
	}, []);

	function grabSelectedUsers() {
		const parentElement = document.getElementById("userSelect");
		const labels = parentElement.children;

		let returnList = [];

		for (const label of labels) {
			const inputElement = label.querySelector("input");

			if (inputElement.checked) {
				let id = inputElement.id;
				id = id.split("|")[1];
				returnList.push(id);
			}
		}

		return returnList;
	}

	async function placeMarketOrder() {
		const inputs = document.querySelectorAll("#MarketOrderDiv> input");

		let bodyData = {};

		const selectedUsers = grabSelectedUsers();

		if (selectedUsers.length === 0) {
			document.getElementById("MarketOrderDebug").innerHTML =
				"Please select users to apply order to.";
			return;
		}

		bodyData["users"] = selectedUsers;

		for (const inp of inputs) {
			bodyData[inp.name] = inp.value;
		}

		console.log(bodyData);

		const request = await fetch(
			"http://localhost:8000/place_iterative_market_order",
			{
				method: "POST",
				headers: {
					Authorization: token,
					"Content-Type": "application/json",
				},
				body: JSON.stringify(bodyData),
			},
		);

		switch (request.status) {
			case 200:
				const response = await request.json();
				document.getElementById("MarketOrderDebug").innerHTML =
					Object.entries(response)
						.map(
							([k, v]) =>
								`${k}: ${Array.isArray(v) ? v.join(" ") : v}`,
						)
						.join("<br>");

				for (const inp of inputs) {
					inp.value = "";
				}

				break;

			case 401:
				alert("Please sign in again, auth failed");
				window.location.href = "/";
				return;

			case 400:
				alert(
					"Unprocessable input, please double check the data in inputs",
				);
				break;

			default:
				break;
		}

	}

	async function placeLimitOrder() {
		const inputs = document.querySelectorAll("#LimitOrderDiv > input");
		let bodyData = {};
		bodyData["users"] = grabSelectedUsers();

		for (const inp of inputs) {
			bodyData[inp.name] = inp.value;
		}

		const request = await fetch(
			"http://localhost:8000/place_iterative_limit_order",
			{
				method: "POST",
				headers: {
					Authorization: token,
					"Content-Type": "application/json",
				},
				body: JSON.stringify(bodyData),
			},
		);

		switch (request.status) {
			case 200:
				const response = await request.json();

				document.getElementById("LimitOrderDebug").innerHTML =
					Object.entries(response)
						.map(
							([k, v]) =>
								`${k}: ${Array.isArray(v) ? v.join(" ") : v}`,
						)
						.join("<br>");

				for (const inp of inputs) {
					inp.value = "";
				}
				break;

			case 401:
				alert("Please sign in again, auth failed");
				window.location.href = "/";
				return;

			case 400:
				alert(
					"Unprocessable input, please double check the data in inputs",
				);
				break;

			default:
				break;
		}
	}

	async function getStockInfo() {
		const bodyData = {
			symbol: document.getElementById("stock_get_info_symbol").value,
		};

		document.getElementById("StockDataOutput").innerHTML = "Please Standby";

		const url = "http://localhost:8000/get-stock-data";

		const request = await fetch(url, {
			method: "POST",
			headers: {
				Authorization: token,
				"Content-Type": "application/json",
			},
			body: JSON.stringify(bodyData),
		});

		switch (request.status) {
			case 400:
				alert("Please fill out all forms in field");
				return;

			case 401:
				alert("Please sign in again, auth failed");
				window.location.href = "/";
				return;

			case 200:
				const data = await request.json();

				document.getElementById("StockDataOutput").textContent =
					JSON.stringify(data["data"]["primaryData"], null, 2);
				
				break;

			default:
				break;
		}
	}

	return (
		<div className={styles.page}>
			<div className={styles.links}>
				<span className={styles.linkDiv}>
					<a href="/user-portal">User Portal</a>
				</span>
				<span className={styles.linkDiv}>
					<a href="/orders">Orders</a>
				</span>
			</div>
			<div className={styles.mainContent}>
				<div className={styles.stockManager}>
					<h1>Stock Search</h1>
					<br />
					<h3>Get Stock Info</h3>
					<input
						type="text"
						id="stock_get_info_symbol"
						placeholder="Enter Stock Symbol"
					/>
					<br />
					<button onClick={getStockInfo}>Get Stock Info</button>
					<br />
					<pre
						className={styles.stockDataOutput}
						id="StockDataOutput"
					>
						Stock Info Output
					</pre>
				</div>
				<div className={styles.ordersDiv}>
					<h1>Place Orders</h1>

					<h3>Select Affected Users</h3>
					<div id="userSelect" className={styles.selectUsersDiv}>
						{usernames.map((name, index) => (
							<label key={index}>
								<input
									type="checkbox"
									id={"usernameboxselect|" + name}
								/>
								{name}
								<br />
							</label>
						))}
					</div>

					<div
						id="MarketOrderDiv"
						className={styles.placeMarketOrderDiv}
					>
						<h3>Place iterative Market Order</h3>
						<input
							type="text"
							placeholder="Enter Stock Symbol"
							name="symbol"
						/>
						<br />
						<input
							type="text"
							placeholder="Enter Stock Qty"
							name="qty"
						/>
						<br />
						<input
							type="text"
							placeholder="Enter Side Choice (buy or sell)"
							name="side"
						/>
						<br />
						<button onClick={placeMarketOrder}>
							Place Market Order
						</button>
						<pre
							className={styles.stockDataOutput}
							id="MarketOrderDebug"
						>
						</pre>
					</div>

					<div id="LimitOrderDiv" className={styles.placeLimitOrder}>
						<h3>Place iterative Limit Order</h3>
						<input
							type="text"
							placeholder="Enter Stock Symbol"
							name="symbol"
						/>
						<br />
						<input
							type="text"
							placeholder="Enter Stock Qty"
							name="qty"
						/>
						<br />
						<input
							type="text"
							placeholder="Enter Side Choice (buy or sell)"
							name="side"
						/>
						<br />
						<input
							type="text"
							placeholder="Enter Limit Price"
							name="limit"
						/>
						<br />
						<button onClick={placeLimitOrder}>
							Place Limit Order
						</button>
						<pre
							className={styles.stockDataOutput}
							id="LimitOrderDebug"
						>
						</pre>
					</div>
				</div>
			</div>
		</div>
	);
}
