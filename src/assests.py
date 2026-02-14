import secrets
import string
import sqlite3
import hashlib

class User :
    def __init__(self, name, api_key, api_secret, paper_trading) :
        self.name = name 
        self.api_key = api_key 
        self.api_secret= api_secret 
        self.paper_trading = paper_trading  

class Error :
    def __init__(self, error_message, error=None) :
        self.error_message = error_message
        self.error= error 

class UserOrder:
    def __init__(self, ordertype, symbol, qty, side, user, client_order_id, transaction_id, date) :
        self.ordertype= ordertype 
        self.symbol= symbol 
        self.qty= qty
        self.side= side 
        self.user = user 
        self.client_order_id = client_order_id 
        self.transaction_id = transaction_id 
        self.date = date

def new_transaction_id():
    characters = string.ascii_letters + string.digits
    transaction_id= ''.join(secrets.choice(characters) for _ in range(16))

    conn = sqlite3.connect("./db/orders.db")
    cursor = conn.cursor()

    query = f"SELECT 1 FROM orders WHERE transaction_id = ? LIMIT 1"
    
    cursor.execute(query, [transaction_id])
    
    result = cursor.fetchone()

    conn.close()
    
    if result is not None :
        return new_transaction_id()

    return transaction_id 
    
def sha256_encode(data: str) -> str:
    data_bytes = data.encode("utf-8")
    hash_object = hashlib.sha256(data_bytes)
    hex_digest = hash_object.hexdigest()
    return hex_digest

def password_auth(user_password, masterhash) :
    return bool(sha256_encode(user_password) == masterhash)

def create_new_master_token() :
    characters = string.ascii_letters + string.digits
    transaction_id= ''.join(secrets.choice(characters) for _ in range(30))
    
    return transaction_id

