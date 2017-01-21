#create features

#import trade data
url = "https://raw.githubusercontent.com/AdrianGPrado/StockMarket-ML/CK/all_quotes.csv"
quotes = pd.read_csv(url,index_col=0,parse_dates=[0], sep='\t', encoding='utf-8')

