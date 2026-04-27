"use client";

import { useEffect, useState, useRef } from "react";
import styles from "./page.module.css";

export default function Home() {
	const originalOptionsRef = useRef(null);
	const [usernames, setUsernames] = useState(["please,", "wait"]);
	const [token, setToken] = useState("");
	const [loadedOptions, setLoadedOptions] = useState({});

	useEffect(() => {
		const token = sessionStorage.getItem("token");

		if (token === null) {
			window.location.href = "/";
		}

		setToken(token);

		async function get_users() {
			const url = "/get-all-users";
			const request = await fetch(url, {
				method: "GET",
				headers: {
					Authorization: token,
				},
			});

			const response = await request.json();

			switch (request.status) {
				case 200:
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
			"/place_iterative_market_order",
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
			"/place_iterative_limit_order",
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

	async function optionsTradeSearch() {
		const symbol = document.getElementById("optionsSymbol").value;
		if (symbol === "") {
			alert("Please fill out fields");
			return;
		}

		const url = "/options-trade-search";
		const request = await fetch(url, {
			method: "POST",
			headers: {
				Authorization: token,
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ symbol: symbol }),
		});

		switch (request.status) {
			case 422:
				const errorStatus = (await request.text()) || null;
				alert(errorStatus);
				break;

			case 401:
				alert(
					"Please make sure a user exists currently in the database, and login again.",
				);
				window.location.href = "/";
				break;

			case 500:
				alert(
					"internal server error contact developer with details of receiving this message. Aidanbruner789@gmail.com",
				);
				break;

			case 200:
				const blob = await request.json();
				console.log(blob);
				setLoadedOptions(blob);
				originalOptionsRef.current = blob;
				break;

			default:
				break;
		}
	}

	function dateFilter() {
		const year = document.getElementById("optionSearchYear").value;
		const month = document.getElementById("optionSearchMonth").value;

		if (year === "" || month === "") {
			setLoadedOptions(originalOptionsRef.current);
			return;
		}

		const source = originalOptionsRef.current;

		const filtered = Object.entries(source).filter(([key, value]) => {
			const match = value.match(/\d{4}-\d{2}-\d{2}/);
			if (!match) return false;

			const [y, m] = match[0].split("-").map(Number);

			return y === Number(year) && m === Number(month);
		});

		setLoadedOptions(Object.fromEntries(filtered));
	}

	function grabContract() {
		const selectedContract =
			document.getElementById("optionContracts").value;
		document.getElementById("marketOrderSymbol").value = selectedContract;
		document.querySelector("#LimitOrderDiv input[name='symbol']").value =
			selectedContract;
	}

	async function cancelTransaction() {
		const transaction_id = document.getElementById(
			"cancelTransaction_id",
		).value;
		if (transaction_id === "") {
			alert("Please fill out fields");
			return;
		}

		const url = "/cancel-transaction";
		const request = await fetch(url, {
			method: "POST",
			headers: {
				Authorization: token,
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				transaction_id: transaction_id,
				users: grabSelectedUsers(),
			}),
		});

		switch (request.status) {
			case 200:
				const response = await request.json();
				document.getElementById("CancelOrderOutput").innerHTML =
					Object.entries(response)
						.map(
							([k, v]) =>
								`${k}: ${Array.isArray(v) ? v.join(" ") : v}`,
						)
						.join("<br>");

				break;

			case 401:
				alert("auth issue, please login again");
				window.location.href = "/";
				return;

			default:
				alert(
					"Please contact developer with details of encountering this message.",
				);
				return;
		}
	}

	return (
		<div className={styles.page}>
			<div className={styles.links}>
				<span className={styles.linkDiv}>
					<a href="/user-portal.html">User Portal</a>
				</span>
				<span className={styles.linkDiv}>
					<a href="/orders.html">Orders</a>
				</span>
			</div>
			<div className={styles.mainContent}>
				<div className={styles.optionsOrdersDiv}>
					<h2>Options Trading</h2>
					<label>Search Stock Option Chain</label>
					<br />
					<input
						id="optionsSymbol"
						type="text"
						placeholder="Enter Symbol"
					/>
					<br />
					<button
						className={styles.optionsTradeSearchButton}
						onClick={optionsTradeSearch}
					>
						Search Options Chain
					</button>
					<br />
					<br />

					<div
						id="optionOrderMenu"
						className={styles.optionOrderMenu}
					>
						<div className={styles.optionSearchDiv}>
							<input
								type="text"
								id="optionSearchYear"
								placeholder="year"
							/>
							<input
								type="text"
								id="optionSearchMonth"
								placeholder="month"
							/>
							<button onClick={dateFilter}>Search</button>
						</div>
						<br />
						<br />
						<select
							id="optionContracts"
							className={styles.optionContracts}
						>
							{Object.keys(loadedOptions).map((obj, ind) => {
								return (
									<option
										value={obj}
										className={styles.optionContract}
										key={ind}
									>
										{loadedOptions[obj]}
									</option>
								);
							})}
						</select>
						<button onClick={grabContract}>Grab Contract</button>
					</div>
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
							id="marketOrderSymbol"
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
						></pre>
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
						></pre>
					</div>
					<div
						id="cancelTransaction"
						className={styles.cancelTransaction}
					>
						<h3>Cancel Transaction</h3>
						<input
							type="text"
							id="cancelTransaction_id"
							placeholder="Enter Transaction ID"
						/>
						<br />
						<button onClick={cancelTransaction}>
							Cancel Orders
						</button>
						<pre
							className={styles.cancelOrderOutput}
							id="CancelOrderOutput"
						></pre>
					</div>
				</div>
			</div>
		</div>
	);
}
