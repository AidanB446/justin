
import requests

data = {
        "users": ["Aidan"],
        "symbol": "AAPL",
        "qty": "5",
        "side": "buy",
        }

headers = {
        "Authorization": "dwAyreGhz95HSpMynbEA3Kgm3KDnd4"

        }


url = "http://localhost:8000/place_iterative_market_order"

request1 = requests.post(url, json=data, headers=headers)

print(request1.status_code)
print("---")

print(request1.text)
print("---")

