
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

url = "http://localhost:8000/get-order-status"

headers = {
        "Authorization": token
        }

requestData = {
        "name": "Aidan", 
        "transaction_id": "bV8MvKbaQy4YAATX",
        }

request2 = requests.post(url, json=requestData, headers=headers)

print(request2.text)


