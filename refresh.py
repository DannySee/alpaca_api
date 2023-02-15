import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import numpy as np
from config import *
import datetime
import json

api = tradeapi.REST(APLACA_API_KEY, APLACA_API_SECRET, ALPACA_API_BASE_URL)


def trends():

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    end_date = yesterday.strftime("%Y-%m-%d")
    start_date = (yesterday - datetime.timedelta(days=2)).strftime("%Y-%m-%d")

    barset = api.get_bars(SYMBOLS,TimeFrame.Day, start_date, end_date).df

    dct = {}
    for smbl in SYMBOLS:
        stonk = barset[(barset.symbol == smbl)]
        median_price = np.mean(stonk.vwap)
        std = np.std(stonk.vwap)
        lower = median_price - std
        upper = median_price + std
        threshold = {
            'upper':upper,
            'lower':lower
        }
        dct[smbl] = threshold

    with open('trends.json','w', encoding='utf-8') as f:
        json.dump(dct, f, ensure_ascii=False, indent=4)


def portfolio():
  
    portfolio = api.list_positions()
    account = api.get_account()

    dct = {}
    for position in portfolio:
        dct[position.symbol] = position.qty
    
    dct['buying_power'] = getattr(account,'regt_buying_power')
    dct['equity'] = getattr(account,'equity')
    with open('portfolio.json','w', encoding='utf-8') as f:
        json.dump(dct, f, ensure_ascii=False, indent=4)


