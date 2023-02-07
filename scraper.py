from pandas_datareader import data as pdr

import yfinance as yf

data = yf.download("^NSEBANK", start="2001-07-01", end="2021-07-30")

data.to_csv("BANKNIFTYfull.csv")