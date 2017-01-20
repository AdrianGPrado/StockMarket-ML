import pandas
import datetime
import pandas_datareader as web

#import trade data
url = "https://raw.githubusercontent.com/AdrianGPrado/StockMarket-ML/CK/trades.csv"
trades = pd.read_csv(url,index_col=0,parse_dates=[0])

#set start and end dates
start = datetime.datetime(2015,11,1)
end = datetime.date.today()

#initialize df
target = web.DataReader("F", 'yahoo', start, end)
target.reset_index(level=0, inplace=True)
target['Ticker'] = ""
target.head()

#initialize empty target DF
target2 = target.ix[:-1]
target2.head()

# trades2.reset_index(level=0, inplace=True)
# trades2 = trades.ix[:5]
trades2 = pd.DataFrame(trades["Ticker"].unique())
# trades2.drop_duplicates(['Ticker'], keep='last')
trades2.columns = ['Ticker']
trades2.head()

for index, row in trades2.iterrows():
    print(row['Ticker'])
    ticker = row['Ticker']
    target_x = web.DataReader(ticker, 'yahoo',start,end)
    target_x['Ticker'] = ticker
    # target_x.reset_index(level=0, inplace=True)
    target2 = target2.append(target_x)



