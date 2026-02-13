
from assests import Error
from assests import new_transaction_id

from database_interactions import insertDBOrder
from database_interactions import get_user_orders_from_transaction_id

from datetime import datetime

from alpaca.common import RawData
from alpaca.common.exceptions import APIError

from alpaca.trading.client import TradingClient
from alpaca.trading.models import Order, Position
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
            
            result = insertDBOrder("limit", stockSymbol, stockOperationQty, side, username, client_order_id, client_transaction_id, date_and_time)
            
            if result != None :
                print(result)
            
            return_data[username] = "order placed"

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


def cancel_order(transaction_id) :
    
    userList = get_user_orders_from_transaction_id(transaction_id) 

    if isinstance(userList, Error) :
        return Error("userList resolved as Error") 
    
    returnData = {}

    for user in userList :
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

        except Exception as e :
            returnData[user.user] = "Cancellation request failed to submit"
            print(e)

    return returnData

def get_stock_position(user, symbol) :
     
    api_key = user.api_key
    api_secret= user.api_secret
    paper_trading_bool = user.paper_trading

    trading_client = None

    try:
        trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

    except APIError as e:
        return Error("Trading Client failed to initialize: ", e)
    

    symbol_position = None 

    try :
        symbol_position= trading_client.get_open_position(symbol)

    except Exception as e :
        return Error("couldn't get open position", e)
    
    return_obj = {}
    
    if isinstance(symbol_position, Position) :

        return_obj["qty"] = symbol_position.qty
        return_obj["qty_available"] = symbol_position.qty_available
        return_obj["symbol"] = symbol_position.symbol
        return_obj["avg_entry_price"] = symbol_position.avg_entry_price
        return_obj["market_value"] = symbol_position.market_value
        return_obj["cost_basis"] = symbol_position.cost_basis
        return_obj["unrealized_pl"] = symbol_position.unrealized_pl
        return_obj["unrealized_intraday_plpc"] = symbol_position.unrealized_intraday_plpc
        return_obj["current_price"] = symbol_position.current_price
        return_obj["lastday_price"] = symbol_position.lastday_price
        return_obj["change_today"] = symbol_position.change_today
        
    else :
        return_obj["qty"] = symbol_position["qty"]
        return_obj["qty_available"] = symbol_position["qty_available"]
        return_obj["symbol"] = symbol_position["symbol"]
        return_obj["avg_entry_price"] = symbol_position["avg_entry_price"]
        return_obj["market_value"] = symbol_position["market_value"]
        return_obj["cost_basis"] = symbol_position["cost_basis"]
        return_obj["unrealized_pl"] = symbol_position["unrealized_pl"]
        return_obj["unrealized_intraday_plpc"] = symbol_position["unrealized_intraday_plpc"]
        return_obj["current_price"] = symbol_position["current_price"]
        return_obj["lastday_price"] = symbol_position["lastday_price"]
        return_obj["change_today"] = symbol_position["change_today"]
        
    return return_obj

