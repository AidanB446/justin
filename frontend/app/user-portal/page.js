"use client";

import styles from "./page.module.css";
import { useState, useEffect } from "react";

export default function UserPortal() {
	const [existingUsers, setExistingUsers] = useState([]);

	useEffect(() => {
		const token = sessionStorage.getItem("token");

		if (token === null) {
			alert("Please sign in again.");
			window.location.href = "/";
		}

		async function loadUsers() {
			try {
				const request = await fetch(
					"http://localhost:8000/get-all-users",
					{
						method: "GET",
						headers: {
							Authorization: token,
						},
					},
				);

				switch (request.status) {
					case 200:
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

				const data = await request.json();
				const userData = data.users || [];

				const users = userData.map((user) => user.name);

				setExistingUsers(users);
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
				alert("Please Fill Out all Form Fields");
				break;
			
			case 409 :
				alert("Account already exists");
				break;

			default:
				alert(
					"site error please contact developer with details on encountering this message",
				);
				break;
		}
	}

	async function modifyUser() {
		const token = sessionStorage.getItem("token");
		// watch for error not sure if needs to be in a use effect

		if (token === null) {
			alert("Please sign in again.");
			window.location.href = "/";
		}

		const username = document.getElementById("user-select");
		const api_key = document.getElementById("mod_api_key");
		const api_secret = document.getElementById("mod_api_secret");
		const paper_trading = document.getElementById("mod_paper_trading");
		
		if ([username.value, api_key.value, api_secret.value].includes("")) {
			alert("Please fill out all forms.");	
			return;	
		}

		const url = "http://localhost:8000/usermod/modify_account";

		const requestData = {
			name: username.value,
			api_key: api_key.value,
			api_secret: api_secret.value,
			paper_trading: paper_trading.checked,
		};

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

			case 400:
				alert("Please fill out all forms of the field");
				break;
	
			case 422 : 
				alert("Please Fill Out all Form Fields");
				break;

			default:
				alert(
					"site error please contact developer with details on encountering this message",
				);
				break;
		}
	}
	
	async function deleteUser() {
	
		const token = sessionStorage.getItem("token");

		if (token === null) {
			alert("Please sign in again.");
			window.location.href = "/";
		}

		const user = document.getElementById("deleteUser-select").value;		
		
		const request = await fetch("http://localhost:8000/usermod/delete_account", {
			method: "POST",
			headers: {
				"Authorization": token,
				"Content-Type": "application/json"
			},
			body : JSON.stringify({"name": user})	
		});

		switch (request.status) {
			case 200:
				window.location.reload();
				break;

			case 400:
				alert("Please fill out all forms of the field");
				break;
			case 401 :
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
	
	function backButton() {
		window.location.href="/home";
	}

	return (
		
		<div>
			<button onClick={backButton} className={styles.backButton}>Back</button>	
			<br/>
			<br/>
			<br/>
			<div className={styles.page}>
				<div className={styles.createNewUser}>
					<h1>Create New User</h1>
					<input type="text" placeholder="Name" id="username" />
					<br />
					<input type="text" placeholder="Api Key" id="api_key" />
					<br />
					<input type="text" placeholder="Api Secret" id="api_secret" />
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

					<h1>Delete User</h1>
					<label>Choose a User </label>
					<select id="deleteUser-select" name="delete-user-select">
						{existingUsers.map((user, ind) => {
							return (
								<option key={ind} value={user}>
									{user}
								</option>
							);
						})}
					</select>
					<br/>
					<button onClick={deleteUser}>Delete User</button>
				</div>
				<div className={styles.modifyExistingUser}>
					<h1>Modify Existing User</h1>
					<label>Choose a User </label>
					<select id="user-select" name="user-select">
						{existingUsers.map((user, ind) => {
							return (
								<option key={ind} value={user}>
									{user}
								</option>
							);
						})}
					</select>
					<br />
					<input type="text" placeholder="Api Key" id="mod_api_key" />
					<br />
					<input type="text" placeholder="Api Secret" id="mod_api_secret" />
					<br />
					<label>
						<input type="checkbox" id="mod_paper_trading" />
						Paper Trading
					</label>
					<br />
					<br />
					<button onClick={modifyUser}>Modify User</button>
					<br />
					<br />
					<p id="mod_debugText"></p>
				</div>
			</div>
		</div>
	);
}
