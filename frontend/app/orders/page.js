"use client";
import Order from "../components/order";
import styles from "./page.module.css";
import { useState } from "react";
export default function OrderManagerPage() {
	const [retrievedOrders, setRetrievedOrders] = useState([
		"Please complete the fields above, and press the Get Orders button to retrieve previous transactions.",
	]);

	function removeOrder(id) {
		setRetrievedOrders((prev) => prev.filter((o) => o[5] !== id));
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
		const orderRows = orders["rows"];
		setRetrievedOrders(orderRows);
	}

	return (
		<div className={styles.page}>
			<button
				onClick={() => {
					window.location.href = "/home";
				}}
				className={styles.backButton}
			>
				Back
			</button>
			<div className={styles.orderManager}>
				<div className={styles.getOrders}>
					<input id="select_year" placeholder="Enter Year of Order" />
					<select id="select_month">
						<option value="">Month</option>
						<option value="01">01</option>
						<option value="02">02</option>
						<option value="03">03</option>
						<option value="04">04</option>
						<option value="05">05</option>
						<option value="06">06</option>
						<option value="07">07</option>
						<option value="08">08</option>
						<option value="09">09</option>
						<option value="09">09</option>
						<option value="10">10</option>
						<option value="11">11</option>
						<option value="12">12</option>
					</select>
					<button onClick={getOrders}>Get Orders</button>
				</div>
				{retrievedOrders.map((orderArr, ind) => {
					return (
						<span key={ind}>
							<Order
								transaction_id={orderArr[6] || null}
								name={orderArr[4] || null}
								client_order_id={orderArr[5]}
								onDelete={removeOrder}	
								pipe={orderArr}
							/>
						</span>
					);
				})}
			</div>
		</div>
	);
}
