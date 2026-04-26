
from assests import Error, User
from assests import new_transaction_id

from database_interactions import insertDBOrder
from database_interactions import get_user_orders_from_transaction_id

from datetime import datetime

from alpaca.common import RawData
from alpaca.common.exceptions import APIError

from alpaca.trading.client import TradingClient
from alpaca.trading.models import Order
from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest 
from alpaca.trading.enums import OrderSide, TimeInForce

import threading

def place_market_order(users, stockSymbol, stockOperationQty, side) :

    orderside = None 

    if side.lower() == "buy" :
        orderside = OrderSide.BUY
    elif side.lower() == "sell" : 
        orderside = OrderSide.SELL
    else :
        return Error("incorrect side in parameter for place_market_order function.")
     
    return_data= {}
    lock = threading.Lock() 

    client_transaction_id = new_transaction_id() 

    def process_request(user) :
        api_key = user.api_key
        api_secret= user.api_secret
        paper_trading_bool = user.paper_trading
        username = user.name     

        trading_client = None

        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

        except APIError as e:
            with lock:  
                return_data[username] = "Trading Client failed to initialize"
            
            return

        market_order_data = MarketOrderRequest(
            symbol=stockSymbol,
            qty=stockOperationQty,
            side=orderside,
            time_in_force=TimeInForce.GTC  
        )

        try:
            market_order = trading_client.submit_order(order_data=market_order_data)
            
            client_order_id = None

            if type(market_order) == RawData :
                client_order_id = market_order["client_order_id"] 
            elif type(market_order) == Order:
                client_order_id = market_order.client_order_id
            
            date_and_time = datetime.now().isoformat()

            result = insertDBOrder("market", stockSymbol, stockOperationQty, side, username, client_order_id, client_transaction_id, date_and_time)
            with lock:
                return_data[username] = "order placed"
        except Exception as e:
            with lock: 
                return_data[username] = f"order failed: {e}"
        

    threads = []
    for user in users :
        t = threading.Thread(target=process_request, args=(user,)) 
        t.start()
        threads.append(t)
    
    for t in threads : 
        t.join()

    return return_data 

def place_limit_order(users, stockSymbol, stockOperationQty, side, limit) :

    orderside = None 

    if side.lower() == "buy" :
        orderside = OrderSide.BUY
    elif side.lower() == "sell" : 
        orderside = OrderSide.SELL
    else :
        return Error("incorrect side in parameter for place_market_order function.")
     
    client_transaction_id = new_transaction_id() 
    
    return_data= {}
    lock = threading.Lock()

    def process_request(user) :
        api_key = user.api_key
        api_secret= user.api_secret
        paper_trading_bool = user.paper_trading
        username = user.name     

        trading_client = None

        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

        except APIError as e:
            with lock:             
                return_data[username] = "Trading Client failed to initialize"
            return

        limit_order_data = LimitOrderRequest(
            symbol=str(stockSymbol),
            limit_price=float(limit),
            qty=int(stockOperationQty),
            side=orderside,
            time_in_force=TimeInForce.GTC,
        )

        try:
            market_order = trading_client.submit_order(order_data=limit_order_data)
            
            client_order_id = None

            if type(market_order) == RawData :
                client_order_id = market_order["client_order_id"] 
            elif type(market_order) == Order:
                client_order_id = market_order.client_order_id

            date_and_time = datetime.now().isoformat()
            
            result = insertDBOrder("limit", stockSymbol, stockOperationQty, side, username, client_order_id, client_transaction_id, date_and_time)
            with lock:     
                return_data[username] = "order placed"

        except Exception as e:
            with lock:  
                return_data[username] = f"order failed: {e}"

    threads = []
    for user in users :
        t = threading.Thread(target=process_request, args=(user,)) 
        t.start()
        threads.append(t) 
    
    for t in threads :
        t.join()

    return return_data

def cancel_orders(users : list[str], transaction_id) :
    
    userList = get_user_orders_from_transaction_id(transaction_id) 
    
    returnData = {}
    lock = threading.Lock()
    
    def process_request(user, users) :
        if user.user not in users :
            return 
    
        userObj = User(user.user)
        userBool = userObj.attempt_getdbinfo()
        if not userBool :
            with lock :
                returnData[user.user] = "user does not exist"
            return 

        api_key = userObj.api_key
        api_secret= userObj.api_secret
        paper_trading_bool = userObj.paper_trading

        trading_client = None

        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

        except APIError as e :
            with lock:  
                returnData[user.user] = f"Trading Client failed to initialize: {e}"
            return 
        
        order = None

        try :
            order= trading_client.get_order_by_client_id(user.client_order_id)
        except Exception as e :
            with lock :
                returnData[user.user] = f"client_order_id no longer active: {e}"
            return 

        order_id = None

        if isinstance(order, Order) :
            order_id = order.id 
        else :
            order_id = order["id"]
        
        try :
            trading_client.cancel_order_by_id(order_id)
            with lock :
                returnData[user.user] = "Cancellation request successfully submitted"

            insertDBOrder("cancel request", user.symbol, user.qty, user.side, user.user, user.client_order_id, user.transaction_id, user.date)

        except Exception as e :
            with lock :
                returnData[user.user] = f"Cancellation request failed to submit: {e}"
            
    
    threads = []
    for user in userList :
        t = threading.Thread(target=process_request, args=(user, userList)) 
        t.start() 
        threads.append(t)
    
    for t in threads :
        t.join()

    return returnData

def close_position(user, symbol) :
    api_key = user.api_key
    api_secret= user.api_secret
    paper_trading_bool = user.paper_trading
    
    username = user.name

    trading_client = None

    try:
        trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

    except APIError as e:
        return Error("alpaca error", e)
    
    close_position_handle = None
   
    try :
        close_position_handle = trading_client.close_position(symbol)        

    except Exception as e:
        return Error("alpaca error", e)
    
    client_order_id= None
    
    if isinstance(close_position_handle, Order) :
        client_order_id= close_position_handle.client_order_id
    else :
        client_order_id = close_position_handle["client_order_id"]


    client_transaction_id = new_transaction_id() 
    
    date_and_time = datetime.now().isoformat()
   
    insertDBOrder("close position", symbol, "all", "close", username, client_order_id, client_transaction_id, date_and_time)


