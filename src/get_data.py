
import requests
import sqlite3
from alpaca.common.exceptions import APIError

from alpaca.data.requests import StockLatestTradeRequest
from alpaca.data.historical import StockHistoricalDataClient

from alpaca.trading.client import TradingClient

from alpaca.trading.models import Order, TradeAccount
from alpaca.common import RawData

from alpaca.trading.models import Order, Position

from assests import Error, User



def get_latest_price(user, stockSymbols) :
    api_key = user.api_key  
    api_secret= user.api_secret
    
    try :
        client = StockHistoricalDataClient(api_key, api_secret)
    except APIError as e :
        raised_error = Error("alpaca error", e)        
        return raised_error 

    request_params = StockLatestTradeRequest(symbol_or_symbols=stockSymbols)
    
    latest_trade_data = None

    try :
        latest_trade_data = client.get_stock_latest_trade(request_params)
    except APIError as e :
        return Error("alpaca error", e)
    
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
        return Error("alpaca error", e)
        
    order = None

    try :
        order = trading_client.get_order_by_client_id(order_client_id)
    except Exception as e: 
        return Error("alpaca error", e)
        
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

def get_stock_position(user, symbol) :
     
    api_key = user.api_key
    api_secret= user.api_secret
    paper_trading_bool = user.paper_trading

    trading_client = None

    try:
        trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)

    except APIError as e:
        return Error("alpaca error", e)
    

    symbol_position = None 

    try :
        symbol_position= trading_client.get_open_position(symbol)

    except Exception as e :
        return Error("alpaca error", e)
    
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

def get_stock_info(symbol) :

    name = Error
    
    conn = sqlite3.connect("./db/accounts.db") 
    cur = conn.cursor()

    cur.execute("SELECT name FROM accounts")    

    name = str(cur.fetchone()[0])

    user = User(name) 
    user.attempt_getdbinfo()

    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest"

    headers = {
        "APCA-API-KEY-ID": user.api_key,
        "APCA-API-SECRET-KEY": user.api_secret 
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200 :
        return Error("status code other than 200 on post request")

    raw_data = response.json()

    parsed_data = {
        "ticker_symbol": raw_data["symbol"],
        "trade_price_usd": raw_data["trade"]["p"],
        "trade_size_shares": raw_data["trade"]["s"],
        "trade_timestamp_utc": raw_data["trade"]["t"],
        "trade_exchange_code": raw_data["trade"].get("x"),
        "trade_id": raw_data["trade"].get("i"),
        "trade_conditions": raw_data["trade"].get("c")
    }
    
    return parsed_data

def get_buying_power(user) :

    api_key = user.api_key
    api_secret= user.api_secret
    paper_trading_bool = user.paper_trading

    accountData= None

    try:
        trading_client = TradingClient(api_key, api_secret, paper=paper_trading_bool)
        
        accountData = trading_client.get_account()

    except APIError as e:
        return Error("alpaca error", e)
    
    buying_power = None
    cash = None

    if isinstance(accountData, TradeAccount) :
        buying_power = accountData.buying_power
        cash = accountData.cash

    else  :
        buying_power = accountData["buying_power"]
        cash = accountData["cash"]
    
    return {"cash": cash, "buying_power": buying_power}

