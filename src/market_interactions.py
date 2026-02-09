
from alpaca.common import RawData
from alpaca.trading.client import TradingClient
from alpaca.trading.models import Order
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from utils import Error

from alpaca.common.exceptions import APIError

from database_interactions import insertDBOrder

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

            # log order to the database here 
            result = insertDBOrder("market", stockSymbol, stockOperationQty, side, username, client_order_id)
            
            if result != None :
                print(result)
            
            return_data[username] = "success"

        except Exception as e:
            print(f"Failed to submit order: {e}")
            return_data[username] = "order failed"

    return return_data 

