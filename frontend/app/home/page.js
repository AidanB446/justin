"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

import Order from "../components/order";

export default function Home() {
	const [users, setUsers] = useState([]);
	const [usernames, setUsernames] = useState([]);
	const [token, setToken] = useState("");

	const [retrievedOrders, setRetrievedOrders] = useState([
		"Please complete the fields above, and press the Get Orders button to retrieve previous transactions.",
	]);

	useEffect(() => {
		const token = sessionStorage.getItem("token");

		if (token === null) {
			window.location.href = "/";
		}

		setToken("token");

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

		async function getOrders() {}

		get_users();
		getOrders();
	}, []);

	function grabSelectedUsers() {
		const parentElement = document.getElementById("userSelect");
		const labels = parentElement.children;

		let returnList = [];

		for (const label of labels) {
			const inputElement = label.querySelector("input");

			if (inputElement.checked) {
				let id = inputElement.id;
				id = id.split("_")[1];
				returnList.push(id);
			}
		}

		return returnList;
	}

	async function placeMarketOrder() {
		const inputs = document.querySelectorAll("#MarketOrderDiv> input");

		let bodyData = {};

		bodyData["users"] = grabSelectedUsers();

		for (const inp of inputs) {
			bodyData[inp.name] = inp.value;
		}

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

		const response = await request.json();
		document.getElementById("MarketOrderDebug").innerHTML =
			JSON.stringify(response);

		for (const inp of inputs) {
			inp.value = "";
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

		const response = await request.json();

		document.getElementById("LimitOrderDebug").innerHTML =
			JSON.stringify(response);

		for (const inp of inputs) {
			inp.value = "";
		}
	}

	async function getOrders() {
		const usertoken = sessionStorage.getItem("token");

		if (usertoken === null) {
			window.location.href = "/";
		}

		const month = document.getElementById("select_month").value;
		const year = document.getElementById("select_year").value;

		if (month === "" || year === "") {
			alert("Please select a month, and year");
			return;
		}

		const getOrdersRequest = await fetch(
			"http://localhost:8000/get-transactions",
			{
				method: "POST",
				headers: {
					Authorization: usertoken,
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ year: year, month: month }),
			},
		);

		switch (getOrdersRequest.status) {
			case 400:
				alert(
					"Bad or no data given, please fill out the input boxes. (only numbers)",
				);
				return;

			case 401:
				alert("Auth failed, please login again.");
				window.location.href = "/";
				return;

			default:
				break;
		}

		const orders = await getOrdersRequest.json();
		setRetrievedOrders(orders["rows"]);
		console.log(orders);
	}

	async function cancelOrder() {
		const user_token = sessionStorage.getItem("token") || null;

		if (user_token === null) {
			alert("Please login again");
			window.location.href = "/";
			return;
		}
		const bodyData = {
			transaction_id: document.getElementById(
				"cancelorder_transaction_id",
			).value,
			users: grabSelectedUsers(),
		};
		const url = "http://localhost:8000/cancel-order";
		const request = await fetch(url, {
			method: "POST",
			headers: {
				Authorization: user_token,
				"Content-Type": "application/json",
			},
			body: JSON.stringify(bodyData),
		});

		switch (request.status) {
			case 400:
				alert("Please fill out all body information to submit request");
				break;

			case 401:
				alert("Please login again");
				window.location.href = "/";
				return;

			case 200:
				document.getElementById("cancelOrderOutput").value =
					JSON.stringify(await request.json());
				break;

			default:
				break;
		}
	}

	return (
		<div className={styles.page}>
			<div className={styles.links}>
				<span className={styles.userDiv}>
					<a href="/user-portal">User Portal</a>
				</span>
				<span className={styles.userDiv}>
					<a href="/orders">Orders</a>
				</span>
			</div>
			<div className={styles.mainContent}>
				<div className={styles.stockManager}>
					<h1>Stock Search</h1>		

				</div>
				<div className={styles.ordersDiv}>
					<h1>Place Orders</h1>

					<h3>Select Affected Users</h3>
					<div id="userSelect" className={styles.selectUsersDiv}>
						{usernames.map((name, index) => (
							<label key={index}>
								<input
									type="checkbox"
									id={"usernameboxselect_" + name}
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
						<p style={{ color: "red" }} id="MarketOrderDebug"></p>
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
						<p style={{ color: "red" }} id="LimitOrderDebug"></p>
					</div>
					<div id="cancelOrderDiv">
						<h3>Cancel Order</h3>
						<input
							type="text"
							placeholder="Enter Transaction ID"
							name="limit"
							id="cancelorder_transaction_id"
						/>
						<br />
						<button onClick={cancelOrder}>Cancel Order</button>
						<p style={{ color: "red" }} id="cancelOrderOutput"></p>
					</div>
				</div>
			</div>
		</div>
	);
}
