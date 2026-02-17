
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

def create_account(user) :
    
    name = user.name    
    api_key = user.api_key
    api_secret = user.api_secret
    paper_trading = user.paper_trading

    conn = sqlite3.connect(db_directory_path + "accounts.db")

    cur = conn.cursor() 

    try :
        cur.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", [api_key, api_secret, name, int(paper_trading)])

    except Exception as e:
        return_error = Error("error inserting new order", error=e)         
        return return_error

    conn.commit() 
    cur.close()
    conn.close()

def delete_account(username) :
   
    conn = sqlite3.connect(db_directory_path + "accounts.db")

    cur = conn.cursor() 

    try :
        cur.execute("DELETE FROM accounts WHERE name = ?", [username])

    except Exception as e:
        return_error = Error("error attempting to delete user", error=e)         
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

def read_master_hash(masteruser) :

    conn = sqlite3.connect(db_directory_path + "master.db") 

    cur = conn.cursor()
    
    cur.execute("SELECT hash_password FROM master WHERE username = ?", [masteruser])
    
    queryResponse = cur.fetchone()
    
    cur.close() 
    conn.close()
    
    queryResponse = queryResponse[0] 
    
    return queryResponse

def get_orders_by_time(year, month) :
    
    conn = sqlite3.connect(db_directory_path + "orders.db")

    cur = conn.cursor()

    cur.execute("SELECT date FROM orders")

    rows = cur.fetchall()
    
    returnRows = [] # rows that were gathered

    for row in rows :
        dateString = None

        try : 
            dateString = row[0]
            if dateString == None :
                # find better solution for error handling
                continue

        except Exception as _ :
            # find better solution for error handling
            continue  

        dateString = str(dateString) 
        dateString = dateString.split("T")[0]
            
        # atp dateString looks like "2000-02-13"
        year = int(dateString.split("-")[0])
        month = int(dateString.split("-")[1])

        print(year, month)
    
        # TODO
        # make sure you compare user input with db data as integers for accuracy


    cur.close()
    conn.close()



