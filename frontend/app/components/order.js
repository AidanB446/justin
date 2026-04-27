"use client";

import styles from "./order.module.css";
import { useRef, useState } from "react";

export default function Order(props) {
	const domain = "https://brunercloud.org/"

	const dataBox = useRef(null);
	const statusOutput = useRef(null);
	const [rawDataToggle, setRawDataToggle] = useState(false);
	const original_pipe = props.pipe;

	if (typeof props.pipe === "string") {
		return <div className={styles.order}>{props.pipe}</div>;
	}

	const newArr = [...props.pipe.slice(0, 5), ...props.pipe.slice(6)];

	async function getOrderStatus() {
		const token = sessionStorage.getItem("token") || null;

		if (token === null) {
			alert("Please sign in");
			window.location.href = "/";
		}

		const url = domain + "/get-order-status";
		const bodyData = {
			name: props.name,
			transaction_id: props.transaction_id,
		};

		const request = await fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: token,
			},
			body: JSON.stringify(bodyData),
		});

		let data = {};

		switch (request.status) {
			case 200:
				data = await request.json();
				if (statusOutput.current) {
					statusOutput.current.innerHTML = Object.entries(data)
						.map(
							([k, v]) =>
								`${k}: ${Array.isArray(v) ? v.join(" ") : v}`,
						)
						.join("<br>");

					break;
				}

				break;

			case 401:
				alert("Please login again");
				window.location.href = "/";
				return;

			case 422:
				data = await request.json();
				alert(data["error"]);
				break;

			default:
				data = await request.json();
				alert(data["error"]);
				alert(
					"Please contact developer with details about getting this message.",
				);
				break;
		}
	}
	
	async function deleteOrder() {

		const token = sessionStorage.getItem("token") || null;

		if (token === null) {
			alert("Please sign in");
			window.location.href = "/";
		}

		const url = domain + "/delete-order"
	
		const requestData = {"client_order_id": props.client_order_id};
		const request = await fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"Authorization": token,
			},
			body: JSON.stringify(requestData)
		});

		switch (request.status) {
			case 401:
				alert("Please login again");
				window.location.href = "/";
				return;

			case 200 :
   				props.onDelete(props.client_order_id);
				return;

			default:
				break;
		}
	}

	function toggleData() {
		if (!rawDataToggle) {
			dataBox.current.innerHTML = original_pipe.join(" | ");
			setRawDataToggle(true);
		} else {
			dataBox.current.innerHTML = newArr.join(" | ");
			setRawDataToggle(false);
		} 
	}

	return (
		<div className={styles.order}>
			<span ref={dataBox}>{newArr.join(" | ")}</span>
			<span className={styles.orderStatus}>
				<button onClick={getOrderStatus}>Get Order Status</button>
				<pre
					className={styles.stockDataOutput}
					ref={statusOutput}
				></pre>
			</span>
			<button onClick={deleteOrder}>
				Delete Order
			</button>	
			<button onClick={toggleData}>Toggle Data</button>	
		</div>
	);
}
