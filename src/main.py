
from user import User
from get_data import get_latest_price

if __name__ == "__main__":
    api_key = "PKFASBVDSGPYDR4G7QPWCR47QD"
    api_secret = "BLqWTrzdvWdMDFmbRTenQM16goyZ1mJR8fK86qkEkRR2"

    user = User(api_key=api_key, api_secret=api_secret, paper_trading=True) 
    
    print(get_latest_price(user, ["AAPL", "TSLA", "MCSF"]))


