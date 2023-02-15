import alpaca_trade_api as tradeapi
from config import *

# authentication and connection details
api_key = APLACA_API_KEY
api_secret = APLACA_API_SECRET
base_url = ALPACA_API_BASE_URL

# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')


def buy(symbol, qty):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side="buy",
        type="market",
        time_in_force='gtc'
    )

    return 200


def sell(symbol, qty):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side="sell",
        type="market",
        time_in_force='gtc'
    )

    return 200


