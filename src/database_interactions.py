
import sqlite3

from assests import Error, UserOrder

db_directory_path = "./db/"

def get_all_users() :
    conn = sqlite3.connect(db_directory_path + "accounts.db")

    cur = conn.cursor() 

    cur.execute("SELECT * FROM accounts", )
    
    users : list[dict] = []
    userRows = cur.fetchall()

    for row in userRows :
        userDict = {
            "api_key" : row[0],
            "api_secret" : row[1],
            "name" : row[2],
            "paper_trading" : row[3],
        }

        users.append(userDict)
        
    return users

def check_if_user_exists(username) :
    conn = sqlite3.connect(db_directory_path + "accounts.db")

    cur = conn.cursor() 

    cur.execute(
	    "SELECT EXISTS(SELECT 1 FROM accounts WHERE name = ? )",
	    [username]
    )
    
    response = cur.fetchone()
    
    return bool(response[0])

def insertDBOrder(ordertype, symbol, qty, side, user, client_order_id, transaction_id, date) :
    conn = sqlite3.connect(db_directory_path + "orders.db")

    cur = conn.cursor() 

    cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [ordertype, symbol, str(qty), side, user, client_order_id, transaction_id, str(date)])

    conn.commit() 
    cur.close()
    conn.close()

def create_account(user) :
    
    nameWhitelist = [""]

    name = user.name    
    api_key = user.api_key
    api_secret = user.api_secret
    paper_trading = user.paper_trading
    
    if name in nameWhitelist :
        return Error("Name Already Taken")

    conn = sqlite3.connect(db_directory_path + "accounts.db")

    cur = conn.cursor() 

    cur.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", [api_key, api_secret, name, int(paper_trading)])

    conn.commit() 
    cur.close()
    conn.close()

def delete_account(username) :
   
    conn = sqlite3.connect(db_directory_path + "accounts.db")

    cur = conn.cursor() 

    cur.execute("DELETE FROM accounts WHERE name = ?", [username])

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

        newOrder = UserOrder(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])     
        
        returnOrders.append(newOrder)
    
    return returnOrders

def get_orders_by_time(year, month):
    month_str = f"{int(month):02d}"
    year_str = str(int(year))
    
    conn = sqlite3.connect(db_directory_path + "orders.db")
    cur = conn.cursor()

    query = """
        SELECT * FROM orders 
        WHERE strftime('%Y', date) = ? 
        AND strftime('%m', date) = ?
    """
    
    cur.execute(query, (year_str, month_str))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


