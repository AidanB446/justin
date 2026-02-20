'use client'

import {useEffect, useState} from "react";
import styles from "./page.module.css";

import User from "../components/user";

export default function Home() {
	
	const [users, setUsers] = useState([])

	useEffect(() => {
		
		const token = sessionStorage.getItem("token");

		if (sessionStorage.getItem("token") === null) {
			window.location.href = "/";
		}	
		
		async function get_users() {
			
			const url = "http://localhost:8000/get-all-users"	
			const request = await fetch(url, {
				method: "GET",	
				headers: {
					"Authorization": token,
				}
			});
			
			const response = await request.json();	
				
			switch (request.status) {
				case 200 : 
					setUsers(response["users"]);
					console.log(response["users"]);
					break;
			
				case 401 :
					alert("Auth no longer valid please sign in again");
					window.location.href = "/";
					break;

				default :
					alert("Internal applciation error please contact developer with details on how you encountered this message.")
			}
			

		}

		get_users();
	}, []);

	return (
		<div>
			<div className={styles.userDiv}>
				
				<a href="/user-portal">User Portal</a>

				<h2>Registered Accounts</h2>
						
				{users.map((obj, _) => (
					<User key={obj.api_key} api_key={obj.api_key} api_secret={obj.api_secret} username={obj.name} paper_trading={obj.paper_trading} />
				))}


			</div>

		</div>
	);

}



