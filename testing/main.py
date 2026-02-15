
import requests

data = {
        "users": ["Aidan"],
        "symbol": "AAPL",
        "qty": "5",
        "side": "buy",
        "limit": "192.57",
        }

headers = {
        "Authorization" : "tgO7mjRWAGLdOUHyTFtFYSz48YEDfO",

        }


url = "http://localhost:8000/place_iterative_limit_order"

request1 = requests.post(url, json=data, headers=headers)

print(request1.status_code)
print("---")

print(request1.text)
print("---")

