
from flask import Flask, request 
from flask_cors import CORS

from database_interactions import create_account, delete_account, read_master_hash
from market_interactions import place_market_order

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

    if not supplied_token == CURRENT_MASTER_TOKEN :
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

    if not supplied_token == CURRENT_MASTER_TOKEN :
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

print(CURRENT_MASTER_TOKEN)

app.run(port=8000)
