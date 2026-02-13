
from assests import Error, User
from market_interactions import close_position

if __name__ == "__main__":
    api_key = "PKFASBVDSGPYDR4G7QPWCR47QD"
    api_secret = "BLqWTrzdvWdMDFmbRTenQM16goyZ1mJR8fK86qkEkRR2"
    name = "Aidan"

    user1 = User(name, api_key=api_key, api_secret=api_secret, paper_trading=True) 

    output = close_position(user1, "AAPL") 
        
    if isinstance(output, Error) :
        print(output.error_message)
        print("--") 
        print("--") 
        print(output.error)

