import yfinance as yf
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from config import access_token, accountID


# Função para obter dados de velas
def get_candles(n):

    client = CandleClient(access_token, real=False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles


# Função para gerar sinais
def signal_generator(open, close, previous_open, previous_close):
    # Bearish Pattern
    if (open > close and
            previous_open < previous_close and
            close < previous_open and
            open >= previous_close):
        return 1

    # Bullish Pattern :) :)
    elif (open < close and
          previous_open > previous_close and
          close > previous_open and
          open <= previous_close):
        return 2

    # No clear pattern
    else:
        return 0


# Função para executar operações de negociação
def execute_trade(signal, dfstream):
    SLTPRatio = 2.
    previous_candleR = abs(dfstream['High'].iloc[-2] - dfstream['Low'].iloc[-2])

    SLBuy = float(dfstream['Open'].iloc[-1]) - previous_candleR
    SLSell = float(dfstream['Open'].iloc[-1]) + previous_candleR

    TPBuy = float(dfstream['Open'].iloc[-1]) + previous_candleR * SLTPRatio
    TPSell = float(dfstream['Open'].iloc[-1]) - previous_candleR * SLTPRatio

    print(dfstream.iloc[:-1, :])
    print(TPBuy, "  ", SLBuy, "  ", TPSell, "  ", SLSell)

    # Sell
    if signal == 1:
        mo = MarketOrderRequest(instrument="EUR_USD", units=-1000,
                                takeProfitOnFill=TakeProfitDetails(price=TPSell).data,
                                stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
    # Buy
    elif signal == 2:
        mo = MarketOrderRequest(instrument="EUR_USD", units=1000,
                                takeProfitOnFill=TakeProfitDetails(price=TPBuy).data,
                                stopLossOnFill=StopLossDetails(price=SLBuy).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)


# Função principal
def trading_job():
    candles = get_candles(3)
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

    execute_trade(signal, dfstream.iloc[:-1, :])


# Execução manual
trading_job()

# Comentado para evitar execução automática
# scheduler = BlockingScheduler()
# scheduler.add_job(trading_job, 'cron', day_of_week='mon-fri', hour='00-23', minute='1,16,31,46',
#                   start_date='2022-01-12 12:00:00', timezone='America/Chicago')
# scheduler.start()