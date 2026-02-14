
import requests

data = {
        "api_key" : "asdf",
        "api_secret" : "asdf",
        "name" : "John",
        "paper_trading" : "1",
        }

delete_data = {
        "name": "John"
        }

url = "http://localhost:8000/usermod/create_account"
request1 = requests.post(url, json=data)

print("--")
print(request1.status_code)
print("--")
print(request1.text)
print("--")

input("Enter to continue")

url = "http://localhost:8000/usermod/delete_account"

request1 = requests.post(url, json=delete_data)

print("--")
print(request1.status_code)
print("--")
print(request1.text)
print("--")



