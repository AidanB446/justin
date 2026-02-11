
from utils import Error
from database_interactions import insertDBOrder

from datetime import datetime

from alpaca.common import RawData
from alpaca.common.exceptions import APIError

from alpaca.trading.client import TradingClient
from alpaca.trading.models import Order
from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest, GetOrderByIdRequest
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

    for user in users :
            
        api_key = user.api_key
        api_secret= user.api_secret
        paper_trading_bool = user.paper_trading
        username = user.name     

        trading_client = None

        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

        except APIError as e:
            return Error("Trading Client failed to initialize: ", e)

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

            result = insertDBOrder("market", stockSymbol, stockOperationQty, side, username, client_order_id, date_and_time)
            
            if result != None :
                print(result)
            
            return_data[username] = "success"

        except Exception as e:
            print(f"Failed to submit order: {e}")
            return_data[username] = "order failed"

    return return_data 

def place_limit_order(users, stockSymbol, stockOperationQty, side, limit) :

    orderside = None 

    if side.lower() == "buy" :
        orderside = OrderSide.BUY
    elif side.lower() == "sell" : 
        orderside = OrderSide.SELL
    else :
        return Error("incorrect side in parameter for place_market_order function.")
     
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
            return Error("Trading Client failed to initialize: ", e)

        limit_order_data = LimitOrderRequest(
            symbol=stockSymbol,
            limit_price=limit,
            qty=stockOperationQty,
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
            
            result = insertDBOrder("limit", stockSymbol, stockOperationQty, side, username, client_order_id, date_and_time)
            
            if result != None :
                print(result)
            
            return_data[username] = "success"

        except Exception as e:
            print(f"Failed to submit order: {e}")
            return_data[username] = "order failed"

    return return_data

def get_order_info(user, order_client_id) :
    
    api_key = user.api_key
    api_secret= user.api_secret
    paper_trading_bool = user.paper_trading
    username = user.name     

    trading_client = None

    try:
        trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

    except APIError as e:
        return Error("Trading Client failed to initialize: ", e)

    order = trading_client.get_order_by_client_id(order_client_id)
        
    order_data = {}

    if type(order) == Order :
        order_data["username"] = username
        order_data["type"] = str(order.type)   
        order_data["status"] = order.status
        order_data["symbol"] = order.symbol 
        order_data["qty"] = order.qty
        order_data["side"] = str(order.side) 

        if order.type == "limit" :
            order_data["limit_price"] = order.limit_price

    elif type(order) == RawData :
        order_data["username"] = username
        order_data["type"] = str(order["type"])   
        order_data["status"] = order["status"]
        order_data["symbol"] = order["symbol"]
        order_data["qty"] = order["qty"]
        order_data["side"] = str(order["side"]) 
        
        if order["type"]== "limit" :
            order_data["limit_price"] = order["limit_price"]

    return order_data

def get_order_status(user, order_client_id) :
    
    api_key = user.api_key
    api_secret= user.api_secret
    paper_trading_bool = user.paper_trading

    trading_client = None

    try:
        trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

    except APIError as e:
        return Error("Trading Client failed to initialize: ", e)
        

    try :
        order = trading_client.get_order_by_client_id(order_client_id)
    
    except Exception as e :
        return_error = Error("Error getting order by client id", e)
        return return_error

    orderstatus = None 

    if type(order) == Order :
        orderstatus = order.status

    elif type(order) == RawData :
         orderstatus = order["status"]
    else :
        return_error = Error("order resolved to a invalid datatype")
        return return_error

    return orderstatus
        

