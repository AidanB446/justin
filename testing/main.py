
import requests

url = "http://localhost:8000/login"

login_attempt = {
        "password": "password",
        }

request1 = requests.post(url, json=login_attempt)

user_token = request1.json()["token"]





