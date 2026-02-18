'use client'

import styles from "./page.module.css";

export default function Home() {
	
	async function start() {
		
		const url = "http://localhost:8000/login"
		
		const password = document.getElementById("passwordinp").value;
		
		const data = {
			"password": password
		};
	
		const request = await fetch(url, {
            method: "POST", 
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        });

		const response = await request.json();
		console.log(response);
		
		if (request.status === 200) {
			sessionStorage.setItem("token", response["token"]);
			window.location.href = "/home";
		} else {
			document.getElementById("debugText").innerHTML = "login failed";
		}
	}

	return (
		<div className={styles.page}>
			<input type="password" id="passwordinp" placeholder="enter password" /><br/>	
			<button onClick={start}>
				start application	
			</button><br/>
			<p id="debugText" className={styles.debugText}></p>

		</div>
	);
}
