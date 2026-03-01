"use client";

import styles from "./order.module.css";

export default function Order(props) {
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

		const url = "http://localhost:8000/get-order-status";
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
				document.getElementById("status_output").innerHTML =
					Object.entries(data)
						.map(
							([k, v]) =>
								`${k}: ${Array.isArray(v) ? v.join(" ") : v}`,
						)
						.join("<br>");

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

	return (
		<div className={styles.order}>
			<span>{newArr.join(" | ")}</span>
			<span className={styles.orderStatus}>
				<button onClick={getOrderStatus}>Get Order Status</button>
				<pre
					className={styles.stockDataOutput}
					id="status_output"
				></pre>
			</span>
		</div>
	);
}
