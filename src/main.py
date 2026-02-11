
from assests import User
from market_interactions import place_market_order

if __name__ == "__main__":
    api_key = "PKFASBVDSGPYDR4G7QPWCR47QD"
    api_secret = "BLqWTrzdvWdMDFmbRTenQM16goyZ1mJR8fK86qkEkRR2"
    name = "Aidan"

    user1 = User(name, api_key=api_key, api_secret=api_secret, paper_trading=True) 
    user2 = User(name, api_key=api_key, api_secret=api_secret, paper_trading=True) 
  
    output1 = place_market_order([user1, user2], "AAPL", 5, "buy")

    print(output1)



   

