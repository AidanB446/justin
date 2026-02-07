
from alpaca.trading.client import TradingClient

api_key = "PKFASBVDSGPYDR4G7QPWCR47QD"
api_secret = "BLqWTrzdvWdMDFmbRTenQM16goyZ1mJR8fK86qkEkRR2"

trading_client = TradingClient(api_key, api_secret, paper=True)

assests = trading_client.get_all_assets()

print(assests)


