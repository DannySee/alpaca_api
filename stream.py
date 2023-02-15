from config import *
import websocket, json
from main import buy, sell
import refresh

def symbols():
    symbols = []
    for symbol in SYMBOLS:
        symbols.append(f'AM.{symbol}')

    return symbols


def on_open(ws):
    print("opened")
    auth_data = {
        "action": "auth", 
        "key": APLACA_API_KEY, 
        "secret": APLACA_API_SECRET
    }

    ws.send(json.dumps(auth_data))
    #symbols = symbols()
    listen_message = {"action":"subscribe","bars":SYMBOLS}

    ws.send(json.dumps(listen_message))


def on_message(ws, message):

    if message[:8] != '[{"T":"s':
        with open('trends.json') as data:
            trends = json.load(data)

        with open('portfolio.json') as data:
            portfolio =  json.load(data)

        data = json.loads(message)

        for pnt in data:
            symbol = pnt['S']
            price = pnt['c']
    
            if price <= trends[symbol]['lower']:
                qty = 10
                if symbol in portfolio:
                    positions = int(portfolio[symbol])
                    if positions < 0:
                        qty = (positions * -1) + qty
                    else:
                        qty = 0

                if qty > 0:
                    try:
                        buy(symbol, qty)
                        refresh.portfolio()
                        print(f'buy: {symbol}*{qty} at {price}')
                    except Exception as err:
                        print(f'sell failure: {symbol}*{qty} at {price}\n{err}')
                else:
                    print(f"hold: {symbol} at {price}")

            elif price >= trends[symbol]['upper']:
                qty = 0
                if symbol in portfolio:
                    positions = int(portfolio[symbol])
                    if positions > 0:
                        qty = positions

                if qty > 0:
                    try:
                        sell(symbol, qty)
                        refresh.portfolio()
                        print(f'sell: {symbol}*{qty} at {price}')
                    except Exception as err:
                        print(f'sell failure: {symbol}*{qty} at {price}\n{err}')
                else:
                    print(f"hold: {symbol} at {price}")

            else:
                print(f"hold: {symbol} at {price}")
    else:
        print('connecting')


def on_message2(ws, message):
    print(message)


def on_close(ws):
    print("closed connection")


socket = "wss://stream.data.alpaca.markets/v2/iex"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()
