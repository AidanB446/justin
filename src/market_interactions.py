
from math import log
from assests import Error
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

def place_market_order(users, stockSymbol, stockOperationQty, side) :

    orderside = None 

    if side.lower() == "buy" :
        orderside = OrderSide.BUY
    elif side.lower() == "sell" : 
        orderside = OrderSide.SELL
    else :
        return Error("incorrect side in parameter for place_market_order function.")
     
    return_data= {}

    client_transaction_id = new_transaction_id() 

    for user in users :
            
        api_key = user.api_key
        api_secret= user.api_secret
        paper_trading_bool = user.paper_trading
        username = user.name     

        trading_client = None

        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

        except APIError as e:
            return_data[username] = "Trading Client failed to initialize"
            continue

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
            
            if result != None :
                print(result)
                print(result.error_message)
                print(result.error)
            
            return_data[username] = "order placed"

        except Exception as e:
            return_data[username] = f"order failed: {e}"

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

    for user in users :
            
        api_key = user.api_key
        api_secret= user.api_secret
        paper_trading_bool = user.paper_trading
        username = user.name     

        trading_client = None

        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

        except APIError as e:
            return_data[username] = "Trading Client failed to initialize"
            print(e) 
            continue

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
            
            if result != None :
                print(result)
            
            return_data[username] = "order placed"

        except Exception as e:
            print(f"Failed to submit order: {e}")
            return_data[username] = "order failed: {e}"

    return return_data

def cancel_orders(users : list[str], transaction_id) :
    
    userList = get_user_orders_from_transaction_id(transaction_id) 
    
    returnData = {}

    for user in userList :
        
        if user.user not in users :
            continue

        api_key = user.api_key
        api_secret= user.api_secret
        paper_trading_bool = user.paper_trading

        trading_client = None

        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

        except APIError as e :
            returnData[user.user] = "Trading Client failed to initialize"
            continue 
        
        order = None

        try :
            order= trading_client.get_order_by_client_id(user.client_order_id)
        except Exception as e :
            returnData[user.user] = "client_order_id no longer active"
            continue

        order_id = None

        if isinstance(order, Order) :
            order_id = order.id 
        else :
            order_id = order["id"]
        
        try :
            trading_client.cancel_order_by_id(order_id)
            returnData[user.user] = "Cancellation request successfully submitted"
            
            insertDBOrder("cancel request", user.symbol, user.qty, user.side, user.user, user.client_order_id, user.transaction_id, user.date)

        except Exception as e :
            returnData[user.user] = "Cancellation request failed to submit"
            print(e)

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
   
    log_handler= insertDBOrder("close position", symbol, "all", "close", username, client_order_id, client_transaction_id, date_and_time)

    if isinstance(log_handler, Error) :
        return Error("Couldn't write to db successfully", log_handler.error)

