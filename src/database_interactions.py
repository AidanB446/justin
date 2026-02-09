
import sqlite3

from utils import Error

db_directory_path = "./db/"

def insertDBOrder(ordertype, symbol, qty, side, user, client_order_id) :
    conn = sqlite3.connect(db_directory_path + "orders.db")

    cur = conn.cursor() 
    
    try :
        cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", [ordertype, symbol, str(qty), side, user, client_order_id])

    except Exception as e:
        return_error = Error("error inserting new order", error=e)         
        return return_error

    conn.commit() 
    cur.close()
    conn.close()

