from pandas_datareader import data as pdr

import yfinance as yf

data = yf.download("HDFCBANK.NS", start="2017-01-01", end="2022-04-30")

data.to_csv("hdfc.csv")