
from flask import Flask, request 
from flask_cors import CORS

from database_interactions import create_account, delete_account, read_master_hash

from assests import User, password_auth, sha256_encode

MASTER_HASH = read_master_hash("Justin")

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello() :
    return "site land"

@app.route("/usermod/<method>", methods=["POST"])
def usermod(method) :
    
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

app.run(port=8000)

