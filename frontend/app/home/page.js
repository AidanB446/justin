"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

import User from "../components/user";

export default function Home() {
	const [users, setUsers] = useState([]);
	const [usernames, setUsernames] = useState([]);

	const [token, setToken] = useState("");

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
					"Authorization": token,
					"Content-Type": "application/json",
				},
				body: JSON.stringify(bodyData),
			},
		);

		const response = await request.json();
		document.getElementById("MarketOrderDebug").innerHTML = JSON.stringify(response);

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
					"Authorization": token,
					"Content-Type": "application/json",
				},
				body: JSON.stringify(bodyData),
			},
		);

		const response = await request.json();

		document.getElementById("LimitOrderDebug").innerHTML = JSON.stringify(response);

		for (const inp of inputs) {
			inp.value = "";
		}
	}

	return (
		<div className={styles.page}>
			<div className={styles.userDiv}>
				<a href="/user-portal">User Portal</a>
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

				<div id="MarketOrderDiv" className={styles.placeMarketOrderDiv}>
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
					<p style={{"color": "red"}} id="MarketOrderDebug"></p>
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
					<button onClick={placeLimitOrder}>Place Limit Order</button>
					<p style={{"color": "red"}} id="LimitOrderDebug"></p>
				</div>
			</div>
		</div>
	);
}
