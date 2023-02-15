import alpaca_trade_api as tradapi
from alpaca_trade_api import REST
from config import *

api = tradapi.REST(APLACA_API_KEY, APLACA_API_SECRET, ALPACA_API_BASE_URL)

class Account:
    def __init__(self) -> None:
        self.account_number = ''
        self.cash = ''
        self.equity = ''
        self.regt_buying_power = ''

acc = Account()

def accDetails():
    a = api.get_account()
    acc.account_number = getattr(a,'account_number')
    acc.cash = getattr(a,'cash')
    acc.equity = getattr(a,'equity')
    acc.regt_buying_power = getattr(a,'regt_buying_power')

accDetails()


# Get a list of all of our positions.
print(acc.regt_buying_power)

