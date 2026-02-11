
import secrets
import string

import sqlite3


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
    

