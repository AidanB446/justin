
from assests import User
from market_interactions import place_market_order
from database_interactions import get_user_orders_from_transaction_id

if __name__ == "__main__":
    api_key = "PKFASBVDSGPYDR4G7QPWCR47QD"
    api_secret = "BLqWTrzdvWdMDFmbRTenQM16goyZ1mJR8fK86qkEkRR2"
    name = "Aidan"

    user1 = User(name, api_key=api_key, api_secret=api_secret, paper_trading=True) 
    
    transaction_id = "bV8MvKbaQy4YAATX"
    
    output = get_user_orders_from_transaction_id(transaction_id=transaction_id)
    

