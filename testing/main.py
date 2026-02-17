
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

url = "http://localhost:8000/close-position"

headers = {
        "Authorization": token
        }

requestData = {
        "name": "Aidan", 
        "symbol": "boogi",
        }

request2 = requests.post(url, json=requestData, headers=headers)

print(request2.text)


