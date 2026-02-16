
from flask import Flask, jsonify, request 
from flask_cors import CORS

from database_interactions import create_account, delete_account, read_master_hash

from get_data import get_stock_info, get_stock_position

from market_interactions import place_market_order, place_limit_order

from assests import User, password_auth, create_new_master_token, Error

app = Flask(__name__)
CORS(app)

MASTER_HASH = read_master_hash("Justin")
CURRENT_MASTER_TOKEN = create_new_master_token()

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
        new_master_token = create_new_master_token()
        CURRENT_MASTER_TOKEN = new_master_token
        return {"token": new_master_token}, 200
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
            err = create_account(new_user)

            if err != None :
                return  (
                    {"error": "couldn't create a new user, could be due to bad input data"}, # body
                    500, {})

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

            delete_handle = delete_account(username) 

            if delete_handle != None :
                print(delete_handle.error)
                print(delete_handle.error_message)
                return  (
                    {"error": "Internal Server Error, couldn't delete account"}, # body
                    500, {}
                )

            return  ({}, 200, {})

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

    except KeyError as _ :
        return  (
            {"error": "json body missing key data"}, 
            400, 
            {} # headers
        )

    userRegistrationMap = {} 
    userList = [] 

    for user in users :
        newUser = User(user)
        getUserHandle = newUser.attempt_getdbinfo()
        
        if not getUserHandle :
            userRegistrationMap[user] = "user not found" 
            continue
    
        userList.append(newUser) 
        userRegistrationMap[user] = newUser     

    orderHandle = place_market_order(userList, stockSymbol, stockQty, stockSide)

    if isinstance(orderHandle, Error) :
        return  (
            {"error": "function failed due to bad data"}, 
            400, 
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

    except KeyError as _ :
        return  (
            {"error": "json body missing key data"}, 
            400, 
            {} # headers
        )

    userRegistrationMap = {} 
    userList = [] 

    for user in users :
        newUser = User(user)
        getUserHandle = newUser.attempt_getdbinfo()
        
        if not getUserHandle :
            userRegistrationMap[user] = "user not found" 
            continue
    
        userList.append(newUser) 
        userRegistrationMap[user] = newUser     

    orderHandle = place_limit_order(userList, stockSymbol, stockQty, stockSide, stockLimit)

    if isinstance(orderHandle, Error) :
        return  (
            {"error": "function failed due to bad data"}, 
            400, 
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
        return {"error": "couldn't get stock data"}, 503, {}

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
        
        print(position_data.error_message)
        print(position_data.error)

        return {"error": "couldn't get position"}, 400, {}

    return ""


app.run(port=8000)

