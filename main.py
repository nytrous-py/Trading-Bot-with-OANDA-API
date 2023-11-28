# app.py

from flask import Flask, render_template, request
from oanda_candles import Pair, Gran, CandleClient
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitDetails, StopLossDetails
import pandas as pd
from config import access_token, accountID  # Import access_token and accountID from config.py

app = Flask(__name__)

# Function to get candles for a given currency pair
def get_candles(pair, n):
    client = CandleClient(access_token, real=False)
    collector = client.get_collector(pair, Gran.M15)
    candles = collector.grab(n)
    return candles

# Function to generate trading signals
def signal_generator(open, close, previous_open, previous_close):
    # Bearish Pattern
    if (open > close and
            previous_open < previous_close and
            close < previous_open and
            open >= previous_close):
        return 1
    # Bullish Pattern
    elif (open < close and
          previous_open > previous_close and
          close > previous_open and
          open <= previous_close):
        return 2
    # No clear pattern
    else:
        return 0

# Function to execute trades
def execute_trade(client, currency_pair, signal, dfstream):
    SLTPRatio = 2.
    previous_candleR = abs(dfstream['High'].iloc[-2] - dfstream['Low'].iloc[-2])

    SLBuy = float(dfstream['Open'].iloc[-1]) - previous_candleR
    SLSell = float(dfstream['Open'].iloc[-1]) + previous_candleR

    TPBuy = float(dfstream['Open'].iloc[-1]) + previous_candleR * SLTPRatio
    TPSell = float(dfstream['Open'].iloc[-1]) - previous_candleR * SLTPRatio

    # Sell
    if signal == 1:
        mo = MarketOrderRequest(instrument=currency_pair, units=-1000,
                                takeProfitOnFill=TakeProfitDetails(price=TPSell).data,
                                stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
    # Buy
    elif signal == 2:
        mo = MarketOrderRequest(instrument=currency_pair, units=1000,
                                takeProfitOnFill=TakeProfitDetails(price=TPBuy).data,
                                stopLossOnFill=StopLossDetails(price=SLBuy).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)

# Main route for the web interface
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/execute_trade', methods=['POST'])
def execute_trade_route():
    currency_pair = request.form['currency_pair']
    candles = get_candles(currency_pair, 3)
    dfstream = pd.DataFrame(columns=['Open', 'Close', 'High', 'Low'])

    for i, candle in enumerate(candles):
        dfstream.loc[i, ['Open']] = float(candle.bid.o)
        dfstream.loc[i, ['Close']] = float(candle.bid.c)
        dfstream.loc[i, ['High']] = float(candle.bid.h)
        dfstream.loc[i, ['Low']] = float(candle.bid.l)

    dfstream = dfstream.astype(float)

    signal = signal_generator(dfstream['Open'].iloc[-1],
                              dfstream['Close'].iloc[-1],
                              dfstream['Open'].iloc[-2],
                              dfstream['Close'].iloc[-2])

    # OANDA API
    api = API(access_token=access_token)
    execute_trade(api, currency_pair, signal, dfstream.iloc[:-1, :])

    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
