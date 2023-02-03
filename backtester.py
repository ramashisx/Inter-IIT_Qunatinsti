import backtrader as bt
import datetime
import matplotlib
import math
import talib
import numpy as np
import backtrader.analyzers as btanalyzers
import logging
import pandas as pd

class dataFeed(bt.feeds.GenericCSVData):
    params = (
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1)
    )


def backtest15(data,strategy):
    
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.0005)

    data =dataFeed(
            dataname="15m/"+data+".csv",
            timeframe=bt.TimeFrame.Minutes,
#         fromdate = datetime.datetime(2020,12,1),
        todate = datetime.datetime(2020,1,30)
)

    print(data)

    cerebro.adddata(data)
    cerebro.addstrategy(strategy)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
#     cerebro.addanalyzer(btanalyzers.PyFolio, _name='pyfolio')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    thestrats = cerebro.run()
    thestrat = thestrats[0]

    strat = thestrat
#     pyfoliozer = strat.analyzers.getbyname('pyfolio')
#     returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

    print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
    return thestrat.analyzers.mysharpe.get_analysis()['sharperatio'],cerebro.broker.getvalue()-100000.0

def backtestday(data,strategy):
    
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)

    data = bt.feeds.YahooFinanceCSVData(dataname="daydata/"+data+".csv")
    cerebro.broker.setcommission(commission=0.0005)
    cerebro.adddata(data)
    cerebro.addstrategy(strategy)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.DrawDown(),_namee='drawdown')
    # cerebro.addanalyzer(btanalyzers.PyFolio, _name='pyfolio')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    thestrats = cerebro.run()
    thestrat = thestrats[0]

    strat = thestrat
#     pyfoliozer = strat.analyzers.getbyname('pyfolio')
#     returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

    print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot(style='candlestick')

    return thestrat.analyzers.mysharpe.get_analysis()['sharperatio'],cerebro.broker.getvalue()-100000.0