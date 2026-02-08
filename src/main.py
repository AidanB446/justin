
from user import User

if __name__ == "__main__":
    api_key = "PKFASBVDSGPYDR4G7QPWCR47QDasdf"
    api_secret = "BLqWTrzdvWdMDFmbRTenQM16goyZ1mJR8fK86qkEkRR2asdf"

    user = User(api_key=api_key, api_secret=api_secret, paper_trading=True) 

    print(user.get_buying_power())



