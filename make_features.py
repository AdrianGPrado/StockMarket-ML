#create features

import pandas as pd
import numpy as np
from numpy import *
from datetime import datetime
from scipy.signal import argrelextrema

#import trade data
url = "https://raw.githubusercontent.com/AdrianGPrado/StockMarket-ML/CK/all_quotes.csv"
quotes = pd.read_csv(url,index_col=0,parse_dates=[0], sep='\t', encoding='utf-8')


#initialize target DF w/ feature columns
# quotes2 = pd.DataFrame(quotes[:2000])
# quotesAll = quotes2.ix[:0]
quotesAll = quotes.ix[:0]
quotesAll["upper_band"] = ""
quotesAll["lower_band"] = ""
quotesAll["9d"] = ""
quotesAll["21d"] = ""
quotesAll["50d"] = ""
quotesAll["100d"] = ""
quotesAll["200d"] = ""
quotesAll["RSI"] = ""
quotesAll["MACD"] = ""

#create ticker list
tickerList = pd.DataFrame(quotes['Ticker'].unique())
# tickerList = pd.DataFrame(quotes2['Ticker'].unique())
tickerList.columns = ['Ticker']
tickerList

# Define Indicator Functions

##Bollinger_Bands
#==============================================================
# http://quant.stackexchange.com/questions/11264/calculating-bollinger-band-correctly
def Bollinger_Bands(stock_price, window_size, num_of_std):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std  = stock_price.rolling(window=window_size).std()
    upper_band = pd.Series(rolling_mean + (rolling_std*num_of_std))
    lower_band = pd.Series(rolling_mean - (rolling_std*num_of_std))
    bands = pd.concat([upper_band, lower_band], axis=1)
    bands.columns = ['upper_band','lower_band']
    return bands

##RSI
#==============================================================
# http://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas
def RSI(series, period):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = pd.stats.moments.ewma(u, com=period-1, adjust=False) / \
         pd.stats.moments.ewma(d, com=period-1, adjust=False)
    return 100 - 100 / (1 + rs)

##MACD
#==============================================================
# http://stackoverflow.com/questions/38270524/cannot-calculate-macd-via-python-pandas
def MACD(group, nslow=26, nfast=12):
    emaslow = pd.ewma(group, span=nslow, min_periods=1)
    emafast = pd.ewma(group, span=nfast, min_periods=1)
    result = pd.DataFrame({'MACD': emafast-emaslow, 'emaSlw': emaslow, 'emaFst': emafast})
    return result

##Extrema
#==============================================================
#minima & maxima
# def minmax(array):
#     extrema_max = argrelextrema(array.values, np.greater)
#     extrema_min = argrelextrema(array.values, np.less)
#     result = pd.DataFrame({'local_max':extrema_max,'local_min':extrema_min})
#     return result


# Feature Creation on Quotes of Selected Tickers

tstart = datetime.now()
n = len(tickerList)
for index, row in tickerList.iterrows():
    ticker = row['Ticker']
    # subquote = pd.DataFrame(quotes2[quotes2.Ticker == ticker])
    subquote = pd.DataFrame(quotes[quotes.Ticker == ticker])
    series = pd.Series(subquote['Adj Close'])
    #Bollinger Bands
    #==============================================================
    BB = Bollinger_Bands(series, 20, 2)
    subquote["upper_band"] = BB["upper_band"]
    subquote["lower_band"] = BB["lower_band"]
    #Moving averages
    #==============================================================
    subquote["9d"] = np.round(subquote["Adj Close"].rolling(window = 9, center = False).mean(), 2)
    subquote["21d"] = np.round(subquote["Adj Close"].rolling(window = 21, center = False).mean(), 2)
    subquote["50d"] = np.round(subquote["Adj Close"].rolling(window = 50, center = False).mean(), 2)
    subquote["100d"] = np.round(subquote["Adj Close"].rolling(window = 100, center = False).mean(), 2)
    subquote["200d"] = np.round(subquote["Adj Close"].rolling(window = 200, center = False).mean(), 2)
    #RSI
    #==============================================================
    RSIx = RSI(series, 14)
    subquote["RSI"] = RSIx
    #MACD
    #==============================================================    
    MACDx = MACD(series)
    subquote["MACD"] = MACDx["MACD"]
    #Sign-changes
    #==============================================================    
    b = (diff(sign(diff(series))) > 0).nonzero()[0] + 1 # local min
    c = (diff(sign(diff(series))) < 0).nonzero()[0] + 1 # local max
    subquote['min'] = series.iloc[b]
    subquote['max'] = series.iloc[c]
    ## Append DF's
    #==============================================================
    quotesAll = quotesAll.append(subquote)
    print ((float(index)/n)*100)
tend = datetime.now()
print(tend-tstart)


# Validate test data
# test = pd.DataFrame(quotesAll[quotesAll.Ticker == "GGP"])
# test.tail()
len(quotes)==len(quotesAll)
quotesAll.head(100)
quotesAll.describe

##save DF
os.chdir("/Users/Collier/Dropbox/Skills/Python/Projects/Stocks/StockMarket-ML/")
quotesAll.to_csv("all_quotes_features.csv", sep='\t', encoding='utf-8')