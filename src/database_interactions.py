
import sqlite3

from assests import Error, UserOrder

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

def get_user_orders_from_transaction_id(transaction_id) :
    conn = sqlite3.connect(db_directory_path + "orders.db")
    cur = conn.cursor()
    
    cur.execute("SELECT * from orders WHERE transaction_id = ?", [transaction_id])

    rows = cur.fetchall()  
    
    returnOrders = []
    
    for row in rows :
        if None in row  or len(row) < 8:
            return Error("a row with incomplete data was found") 

        newOrder = UserOrder(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])     
        
        returnOrders.append(newOrder)
    
    return returnOrders

