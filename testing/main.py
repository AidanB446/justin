
import requests

logindata = {
        "password": "password"
        }

headers = {
        "Authorization" : "tgO7mjRWAGLdOUHyTFtFYSz48YEDfO",
        }

url = "http://localhost:8000/login"

request1 = requests.post(url, json=logindata)

data = request1.json()

token = data["token"]

url = "http://localhost:8000/get-buying-power"

headers = {
        "Authorization": token,
        "Content-Type": "application/json"
        }

requestData = {
        "users": ["Aidan", "daniel", "asdfsadf"], 
        }

request2 = requests.post(url, json=requestData, headers=headers)

print(request2.status_code)
print(request2.json())

