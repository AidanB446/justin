
from assests import User
from market_interactions import get_stock_position 

if __name__ == "__main__":
    api_key = "PKFASBVDSGPYDR4G7QPWCR47QD"
    api_secret = "BLqWTrzdvWdMDFmbRTenQM16goyZ1mJR8fK86qkEkRR2"
    name = "Aidan"

    user1 = User(name, api_key=api_key, api_secret=api_secret, paper_trading=True) 
    

    get_stock_position(user1, "AAPL")



