
from utils import User
from market_interactions import get_order_info 

if __name__ == "__main__":
    api_key = "PKFASBVDSGPYDR4G7QPWCR47QD"
    api_secret = "BLqWTrzdvWdMDFmbRTenQM16goyZ1mJR8fK86qkEkRR2"
    name = "Aidan"

    user1 = User(name, api_key=api_key, api_secret=api_secret, paper_trading=True) 
    output = get_order_info(user1, "7e49ed1b-eb12-4a00-9853-8028a92fb5f4")
    
    print(output)

