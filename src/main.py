
from os import close
import sqlite3
from flask import Flask, jsonify, request 
from flask_cors import CORS

from database_interactions import check_if_user_exists, create_account, delete_account, get_orders_by_time, get_all_users

from get_data import get_buying_power, get_order_info, get_stock_info, get_stock_position

from market_interactions import close_position, place_market_order, place_limit_order

from assests import User, password_auth, Error

app = Flask(__name__)
CORS(app)

MASTER_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
CURRENT_MASTER_TOKEN = "a28047151d0e56f8dc6292773603d0d6"

@app.route("/")
def hello() :
    return "site land"

@app.route("/login", methods=["POST"])
def login():
    global MASTER_HASH
    global CURRENT_MASTER_TOKEN
    
    data = request.get_json()  

    if not data or "password" not in data:
        return {"error": "json body missing key 'password'"}, 400

    user_password = data["password"]

    if password_auth(user_password, MASTER_HASH):
        return {"token": CURRENT_MASTER_TOKEN}, 200
    else:
        return {"error": "authentication failed"}, 401


@app.route("/usermod/<method>", methods=["POST"])
def usermod(method) :
    
    # auth logic here
    supplied_token = request.headers.get("Authorization") 

    if not supplied_token == CURRENT_MASTER_TOKEN  or supplied_token == None:
        return {"error": "unauthorized"}, 401, {} 

    match method:
        case "create_account" :
            data = request.get_json()
            
            api_key = None
            api_secret = None
            username = None 
            paper_trading = None

            try :
                api_key = data["api_key"]  
                api_secret = data["api_secret"]  
                username = data["name"]
                paper_trading = data["paper_trading"]

            except KeyError as _ :
                return  (
                    {"error": "json body missing key data"}, # body
                    400, 
                    {} # headers
                )

            new_user = User(username, api_key, api_secret, int(paper_trading))
            
            if check_if_user_exists(new_user.name) :
                return  ({"error": "username already exists in db"}, 422, {})

            callHandler = create_account(new_user)
            
            if isinstance(callHandler, Error):
                return  (
                    {"error": "account already exists"}, # body
                    409, 
                    {} # headers
                )

            return  ({}, 200, {})

        case "delete_account":
            data = request.get_json()
            
            username = None

            try :
                username = data["name"]
            except KeyError as _ :
                return  (
                    {"error": "json body missing key data"}, # body
                    400, 
                    {} # headers
                )

            delete_account(username) 
            
            return  ({"flag": "returned_in case delete_account"}, 200, {})
        
        case "modify_account" :
            data = request.get_json()
            
            username = None
            api_key = None            
            api_secret = None
            paper_trading = None 

            try :
                username = data["name"]
                api_key = data["api_key"] 
                api_secret = data["api_secret"]
                paper_trading = data["paper_trading"]

            except KeyError as _ :
                return  (
                    {"error": "json body missing key data"}, # body
                    400, 
                    {} # headers
                )
            
            delete_account(username)             
            
            new_user = User(username, api_key, api_secret, int(paper_trading))
            create_account(new_user) 
           
            return {"status": "success"}, 200, {}


    return ""
    
@app.route("/place_iterative_market_order", methods=["POST"])
def place_iterative_market_order() :
    # auth logic here
    supplied_token = request.headers.get("Authorization") 

    if not supplied_token == CURRENT_MASTER_TOKEN or supplied_token == None:
        return {"error": "unauthorized"}, 401, {} 


    data = request.get_json()
    users = None # list of users names
    stockSymbol = None
    stockQty = None
    stockSide = None

    try :
        users = data["users"] 
        stockSymbol = data["symbol"]
        stockQty = int(data["qty"])
        stockSide = data["side"] 

    except Exception as _ :
        return  (
            {"error": "json body missing key data"}, 
            400, 
            {} # headers
        )

    userRegistrationMap = {} 
    userList = [] 

    for user in users :
        newUser = User(user)
        getUserHandle = newUser.attempt_getdbinfo() # FLAG 500

        if not getUserHandle :
            userRegistrationMap[user] = "user not found" 
            continue
    
        userList.append(newUser) 
        userRegistrationMap[user] = newUser     

    orderHandle = place_market_order(userList, stockSymbol, stockQty, stockSide)

    if isinstance(orderHandle, Error) :
        # bad data 
        return  (
            {"error": "function failed due to bad data"}, 
            422, 
            {} # headers
        )

    return orderHandle, 200, {}

    
@app.route("/place_iterative_limit_order", methods=["POST"])
def place_iterative_limit_order() :
 
    supplied_token = request.headers.get("Authorization") 

    if not supplied_token == CURRENT_MASTER_TOKEN or supplied_token == None:
        return {"error": "unauthorized"}, 401, {} 

    data = request.get_json()
    users = None # list of users names
    stockSymbol = None
    stockQty = None
    stockSide = None
    stockLimit = None    

    try :
        users = data["users"] 
        stockSymbol = data["symbol"]
        stockQty = int(data["qty"])
        stockSide = data["side"] 
        stockLimit = data["limit"] 

    except Exception as _ :
        return  (
            {"error": "json body missing key data"}, 
            400, 
            {} # headers
        )

    userRegistrationMap = {} 
    userList = [] 

    for user in users :
        newUser = User(user)
        
        getUserHandle = newUser.attempt_getdbinfo() # FLAG 500
        
        if not getUserHandle :
            userRegistrationMap[user] = "user not found" 
            continue
    
        userList.append(newUser) 
        userRegistrationMap[user] = newUser     

    orderHandle = place_limit_order(userList, stockSymbol, stockQty, stockSide, stockLimit)

    if isinstance(orderHandle, Error) :
        return  (
            {"error": "function failed due to bad data"}, 
            422, 
            {} # headers
        )

    return orderHandle, 200, {}

@app.route("/get-stock-data", methods=["POST"])
def getstock() :
    
    auth_header = request.headers.get("Authorization") 

    if auth_header != CURRENT_MASTER_TOKEN  or auth_header == None:
        return {"error": "auth failed"}, 401, {}
    
    stockSymbol = None

    try :
        stockSymbol = request.get_json()["symbol"]  
    
    except Exception as _:
        return {"error": "insufficient json body data"}, 400, {}

    stockData = get_stock_info(stockSymbol)   

    if isinstance(stockData, Error) :
        return {"error": stockData.error_message}, 503, {}

    return jsonify(stockData) 

@app.route("/get-stock-position", methods=["POST"])
def get_pos() :
    auth_header = request.headers.get("Authorization") 

    if auth_header != CURRENT_MASTER_TOKEN  or auth_header == None:
        return {"error": "auth failed"}, 401, {}
 
    data = request.get_json()
    
    symbol = None
    username = None

    try :
        username = data["name"]
        symbol = data["symbol"] 
 
    except Exception as _:
        return {"error": "insufficient json body data"}, 400, {}

    newUser = User(username)
    pos_error = newUser.attempt_getdbinfo()

    if isinstance(pos_error, Error) :
        return {"error": "user not found"}, 404, {}
    
    position_data = get_stock_position(newUser, symbol)
    
    if isinstance(position_data, Error) :
        return {"status": position_data.error}, 200, {}

    return position_data, 200, {}

@app.route("/get-order-status", methods=["POST"])
def get_user_order_status() :
    auth_header = request.headers.get("Authorization") 

    if auth_header != CURRENT_MASTER_TOKEN  or auth_header == None:
        return {"error": "auth failed"}, 401, {}
 
    data = request.get_json()
    
    username = None
    transaction_id = None

    try :
        username = data["name"]
        transaction_id = data["transaction_id"]
 
    except Exception as _:
        return {"error": "insufficient json body data"}, 400, {}

    newUser = User(username)
    pos_error = newUser.attempt_getdbinfo()

    if isinstance(pos_error, Error) :
        return {"error": "user not found"}, 404, {}
    
    client_order_id = None
    
    conn = sqlite3.connect("./db/orders.db") 
    
    cur = conn.cursor()

    cur.execute("SELECT client_order_id FROM orders WHERE user = ? AND transaction_id = ?", [username, transaction_id]) 
    
    try :
        client_order_id = cur.fetchone()[0]
    except Exception as _ :
        return {"error": "order not found"}, 404, {}


    cur.close()
    conn.close() 
    
    user = User(username)
    err_result = user.attempt_getdbinfo()
    
    if isinstance(err_result, Error) :
        return {"error": "user not found"}, 404, {}
    
    order_data = get_order_info(user, client_order_id)
   
    if isinstance(order_data, Error) :
        return {"status": order_data.error}, 422, {}

    return order_data, 200, {}

@app.route("/close-position", methods=["POST"])
def close_total_stock_position() :
    
    auth_header = request.headers.get("Authorization") 

    if auth_header != CURRENT_MASTER_TOKEN  or auth_header == None:
            return {"error": "auth failed"}, 401, {}
     
    data = request.get_json() 
    
    users= None
    symbol = None

    try :
        users = data["users"]
        symbol= data["symbol"]
 
    except Exception as _:
        return {"error": "insufficient json body data"}, 400, {}
    
    returnData = {}

    for username in users :

        user = User(username)
        user_init_handle = user.attempt_getdbinfo()
        
        if isinstance(user_init_handle, Error) :
            returnData[username] = "user not found"  
            continue 

        close_position_handle = close_position(user, symbol)
        
        if isinstance(close_position_handle, Error) :
            returnData[username] = "trading client failed to initialize"  
            continue 

        returnData[username] = "success"

    return {"status": returnData}, 200, {}

@app.route("/get-transactions", methods=["POST"])
def get_db_transactions_by_month() :
    auth_header = request.headers.get("Authorization") 

    if auth_header != CURRENT_MASTER_TOKEN  or auth_header == None:
            return {"error": "auth failed"}, 401, {}
     
    data = request.get_json() 
    
    year = None
    month = None

    try :
        year = int(data["year"])
        month = int(data["month"])

    except Exception as _:
        return {"error": "insufficient json body data"}, 400, {}
    
    orders = get_orders_by_time(year, month)    

    return {"rows": orders}, 200, {}

@app.route("/get-all-users", methods=["GET"])
def get_all_users_endpoint12() :
    auth_header = request.headers.get("Authorization") 

    if auth_header != CURRENT_MASTER_TOKEN  or auth_header == None:
            return {"error": "auth failed"}, 401, {}
     
    users = get_all_users() 
    
    buying_power_return= {}

    for user in users :
        username = None
        
        if not isinstance(user, dict) :
            continue

        username = user["name"]
    
        user = User(username)
        user.attempt_getdbinfo()

        buying_power = get_buying_power(user) 

        if isinstance(buying_power, Error) :
            buying_power_return[username] = buying_power.error
            continue
        
        buying_power_return[username] = buying_power 


    return {"users": users, "buying_power": buying_power_return}, 200, {}


app.run(port=8000)


