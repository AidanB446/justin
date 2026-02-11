
import sqlite3

from assests import Error

db_directory_path = "./db/"

def insertDBOrder(ordertype, symbol, qty, side, user, client_order_id, transaction_id, date) :
    conn = sqlite3.connect(db_directory_path + "orders.db")

    cur = conn.cursor() 

    try :
        cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [ordertype, symbol, str(qty), side, user, client_order_id, transaction_id, str(date)])

    except Exception as e:
        return_error = Error("error inserting new order", error=e)         
        return return_error

    conn.commit() 
    cur.close()
    conn.close()

def create_account(name, api_key, api_secret) :

    conn = sqlite3.connect(db_directory_path + "accounts.db")

    cur = conn.cursor() 

    try :
        cur.execute("INSERT INTO accounts VALUES (?, ?, ?)", [api_key, api_secret, name])

    except Exception as e:
        return_error = Error("error inserting new order", error=e)         
        return return_error

    conn.commit() 
    cur.close()
    conn.close()


def get_users_from_transaction_id(transaction_id) :
    
    # return a list of all users who have this transaction_id
    pass







