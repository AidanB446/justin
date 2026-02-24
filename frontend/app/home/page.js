"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

import User from "../components/user";
import {doc} from "prettier";

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
		
	}
	
	async function placeOrder() {
		
		const users = grabSelectedUsers(); // list of usernames
		const stockSymbol = document.getElementById("stockSymbol");
		const stockQty = document.getElementById("stockQty");
		const stockChoice = document.getElementById("stockChoice");

		const bodyData = {
			users: users,
			symbol: document.getElementById("stockSymbol").value,
			qty: document.getElementById("stockQty").value,
			side: document.getElementById("stockChoice").value,
		};

		const request = await fetch(
			"http://localhost:8000/place_iterative_market_order",
			{
				method: "POST",
				headers: {
					Authorization: token,
				},
				body: JSON.stringify(bodyData),
			},
		);

		const response = await request.json();
		console.log(response);
	}

	return (
		<div className={styles.page}>
			<div className={styles.userDiv}>
				<a href="/user-portal">User Portal</a>
				<h2>Registered Accounts</h2>
				{users.map((obj, ind) => (
					<User
						key={ind}
						api_key={obj.api_key}
						api_secret={obj.api_secret}
						username={obj.name}
						paper_trading={obj.paper_trading}
					/>
				))}
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
							<br/>
						</label>
					))}
				</div>
				<div className={styles.mainParent}>
					<h3>Place iterative Market Order</h3>
					<input
						type="text"
						placeholder="Enter Stock Symbol"
						id="stockSymbol"
					/>
					<br />
					<input
						type="text"
						placeholder="Enter Stock Qty"
						id="stockQty"
					/>
					<br />
					<input
						type="text"
						placeholder="Enter Side Choice (buy or sell)"
						id="stockChoice"
					/>
					<br />
				</div>
				<button>Place Limit Order</button>
			</div>
		</div>
	);
}
