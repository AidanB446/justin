
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.requests import OptionChainRequest

API_KEY = "PKK5LVE3RSHVEEKKBQDWWAGQLI"
SECRET_KEY = "FRB8HP18WMd7Tchk3p8TLnmkX6wEvj6jZujC45D1LEFT"

data_client = OptionHistoricalDataClient(API_KEY, SECRET_KEY)

request = OptionChainRequest(
    underlying_symbol="AAPL"
)

chain = data_client.get_option_chain(request)


def parse_option_symbol(symbol):
    underlying = symbol[:4]
    expiration = symbol[4:10]
    opt_type = symbol[10]
    strike = int(symbol[11:]) / 1000

    return {
        "underlying": underlying,
        "expiration": f"20{expiration[:2]}-{expiration[2:4]}-{expiration[4:]}",
        "type": "Call" if opt_type == "C" else "Put",
        "strike": strike,
    }


for contract in chain:
    parsed = parse_option_symbol(contract)

    print(
        f"{parsed['expiration']} | "
        f"{parsed['type']:4} | "
        f"${parsed['strike']:>6} | "
        f"{contract}"
    )


