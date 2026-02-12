
from alpaca.common.exceptions import APIError

from alpaca.data.requests import StockLatestTradeRequest
from alpaca.data.historical import StockHistoricalDataClient

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

