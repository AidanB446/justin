
import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.models import TradeAccount



# still working on error handling for user auth


class User :

    def __init__(self, api_key, api_secret, paper_trading) :
        self.api_key = api_key 
        self.api_secret= api_secret 
        self.paper_trading = paper_trading  
        
        try :
            self.tradeClient = TradingClient(api_key, api_secret, paper=paper_trading) 

        except requests.exceptions.HTTPError :
            print("encountered error")
            self.tradeClient= None


    def get_buying_power(self):
        
        if self.tradeClient == None :
            return str("user not registered" )

        raw_account_data = self.tradeClient.get_account()
        
        if isinstance(raw_account_data, TradeAccount):
            account = raw_account_data
        else:
            account = TradeAccount(**raw_account_data)

        buying_power = account.buying_power
        
        # extra safety
        if buying_power is None :
            return str("error in getting buying power.")

        return float(buying_power) 

    def get_daily_profit(self) :
        pass

    def get_order_status(self, client_transaction_id) :
        pass



