
from alpaca.common.exceptions import APIError

from alpaca.data.requests import StockLatestTradeRequest
from alpaca.data.historical import StockHistoricalDataClient

from alpaca.trading.client import TradingClient

from alpaca.trading.models import Order
from alpaca.common import RawData

from alpaca.trading.models import Order, Position

from assests import Error

def get_latest_price(user, stockSymbols) :
    api_key = user.api_key  
    api_secret= user.api_secret
    
    try :
        client = StockHistoricalDataClient(api_key, api_secret)
    except APIError as e :
        raised_error = Error(e)        
        return raised_error 

    request_params = StockLatestTradeRequest(symbol_or_symbols=stockSymbols)

    latest_trade_data = client.get_stock_latest_trade(request_params)
    
    return_dictionary = {}

    for i in stockSymbols:
        try :
            return_dictionary[i] = latest_trade_data[i].price 
        except KeyError :
            return_dictionary[i] = None 

    return return_dictionary

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

