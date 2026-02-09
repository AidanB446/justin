
from utils import User
from market_interactions import place_limit_order, place_market_order


if __name__ == "__main__":
    api_key = "PKFASBVDSGPYDR4G7QPWCR47QD"
    api_secret = "BLqWTrzdvWdMDFmbRTenQM16goyZ1mJR8fK86qkEkRR2"
    name = "Aidan"

    user1 = User(name, api_key=api_key, api_secret=api_secret, paper_trading=True) 
    user2 = User("Albert", api_key="asdf", api_secret="asdf", paper_trading=True) 
    output = place_limit_order([user1, user2], "AAPL", 1, "buy", 500) 

    print(output)



