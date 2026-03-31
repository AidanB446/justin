"use client";

import User from "../components/user";
import styles from "./page.module.css";
import { useState, useEffect } from "react";

export default function UserPortal() {
	const [users, setUsers] = useState([]);
	const [token, setToken] = useState("");

	useEffect(() => {
		const sesstoken = sessionStorage.getItem("token");

		if (sesstoken === null) {
			alert("Please sign in again.");
			window.location.href = "/";
		}

		setToken(sesstoken);

		async function loadUsers() {
			try {
				const request = await fetch(
					"http://localhost:8000/get-all-users",
					{
						method: "GET",
						headers: {
							Authorization: sesstoken,
						},
					},
				);

				let data = {};

				switch (request.status) {
					case 200:
						data = await request.json();
						setUsers(data["users"]);
						break;

					case 401:
						alert("bad auth please sign in again");
						window.location.href = "/";
						break;

					default:
						alert(
							"site error please contact developer with details on encountering this message",
						);
						break;
				}
			} catch (err) {
				console.error("Error loading users:", err);
			}
		}

		loadUsers();
	}, []);

	async function createNewUser() {
		const token = sessionStorage.getItem("token");
		// watch for error not sure if needs to be in a use effect
		if (token === null) {
			alert("Please sign in again.");
			window.location.href = "/";
		}

		const username = document.getElementById("username");
		const api_key = document.getElementById("api_key");
		const api_secret = document.getElementById("api_secret");
		const paper_trading = document.getElementById("paper_trading");

		if ([username.value, api_key.value, api_secret.value].includes("")) {
			alert("Please fill out all forms.");
			return;
		}

		const requestData = {
			name: username.value,
			api_key: api_key.value,
			api_secret: api_secret.value,
			paper_trading: paper_trading.checked,
		};

		const url = "http://localhost:8000/usermod/create_account";

		const request = await fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: token,
			},
			body: JSON.stringify(requestData),
		});

		switch (request.status) {
			case 200:
				window.location.reload();
				break;

			case 401:
				alert("bad auth please sign in again");
				window.location.href = "/";
				break;

			case 422 :
				alert("Please choose another username, username taken");
				break;

			case 400 :
				alert("Please Fill Out all Form Fields");
				break;

			case 409:
				alert("Account already exists");
				break;

			default:
				alert(
					"site error please contact developer with details on encountering this message",
				);
				break;
		}
	}

	function backButton() {
		window.location.href = "/home.html";
	}
	
	
	if (users.length === 0) {
		return <div>please standby</div>
	}


	return (
		<div>
			<button onClick={backButton} className={styles.backButton}>
				Back
			</button>
			<br />
			<br />
			<br />
			<div className={styles.page}>
				<div className={styles.userIterable}>
					<center>
						<h1>Users Menu</h1>
					</center>
					{users.map((userobj, ind) => {
						return (
							<User
								key={ind}
								username={userobj.name}
								token={token}
								api_key={userobj.api_key}
								api_secret={userobj.api_secret}
								paper_trading={String(
									Boolean(userobj.paper_trading),
								)}
							/>
						);
					})}
				</div>
				<div id="userModDiv" className={styles.userMod}>
					<div className={styles.createNewUser}>
						<h1>Create New User</h1>
						<input type="text" placeholder="Name" id="username" />
						<br />
						<input type="text" placeholder="Api Key" id="api_key" />
						<br />
						<input
							type="text"
							placeholder="Api Secret"
							id="api_secret"
						/>
						<br />
						<label>
							<input type="checkbox" id="paper_trading" />
							Paper Trading
						</label>
						<br />
						<br />
						<button onClick={createNewUser}>Create User</button>
						<br />
						<br />
						<p id="debugText"></p>
					</div>
				</div>
			</div>
		</div>
	);
}
