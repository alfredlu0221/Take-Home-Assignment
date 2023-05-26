from financial.financial_module import get_request
from financial.financial_module import response_normalize
from financial.financial_module import establish_connection
from financial.financial_module import set_database
from financial.financial_module import get_database
import pandas as pd

def get_stock_data(stock_symbols):
  df_stock_transposed = pd.DataFrame()
  for symbol in stock_symbols:
    print('symbol:', symbol)
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + symbol + '&outputsize=compact&apikey=3YREPN7DZKD2QM2L'
    response = get_request(url)
    df_stock_transposed = pd.concat([df_stock_transposed, response_normalize(response)])
  return df_stock_transposed

# define a list of strings
stock_symbols = ["IBM", "AAPL"]
df_stock = get_stock_data(stock_symbols)

# establish connection to sqlite database and save into db
connection, cursor = establish_connection('financial_data.db')
set_database(connection, cursor, df_stock)
get_database()
