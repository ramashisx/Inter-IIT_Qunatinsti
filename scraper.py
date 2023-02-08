# from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf

tickers = pd.read_csv("190.csv")
# tickers = tickers.Tickers

a=0
print(tickers.loc[1])
for i in range(len(tickers)):
    x = str(tickers.loc[i].Company)
    try:
        data = yf.download(x+".NS", start="2014-07-01", end="2017-07-01",interval = '1d')
        data.to_csv("rendidata/period1/"+x+".csv")
        data = yf.download(x+".NS", start="2017-07-01", end="2021-07-01",interval = '1d')
        data.to_csv("rendidata/period2/"+x+".csv")
        data = yf.download(x+".NS", start="2021-07-01", end="2023-02-01",interval = '1d')
        data.to_csv("rendidata/period3/"+x+".csv")
        # print('aa')
    except:
        print(x)