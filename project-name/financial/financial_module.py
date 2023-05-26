import requests
import json
import sqlite3
import pandas as pd
# display all the  rows
pd.set_option('display.max_rows', None)
# display all the  columns
pd.set_option('display.max_columns', None)

def get_request(url):
  try:
    response = requests.get(url)
    response.raise_for_status()
  except requests.exceptions.HTTPError as e:
    print ("HTTPError:",e)
  except requests.exceptions.ConnectionError as e:
    print ("ConnectionError:",e)
  except requests.exceptions.Timeout as e:
    print ("Timeout:",e)
  except requests.exceptions.RequestException as e:
    raise SystemExit(e)
  return response

def response_normalize(response):
  data_dict = response.json()
  df = pd.DataFrame(dict(list(data_dict.get('Time Series (Daily)').items())[:10]))

  df_transposed = df.transpose()
  df_transposed = df_transposed.filter(items=['1. open', '5. adjusted close', '6. volume'])
  df_transposed.reset_index(inplace=True)
  df_transposed.rename(columns={"index": "date", "1. open": "open_price", "5. adjusted close": "close_price", "6. volume": "volume"}, inplace=True)
  df_transposed['symbol'] = data_dict.get('Meta Data').get('2. Symbol')
  df_transposed = df_transposed[ ['symbol'] + [ col for col in df_transposed.columns if col != 'symbol' ] ]

  pretty = json.dumps(df_transposed.to_dict('records'), indent=4)
  print(pretty)
  return df_transposed

def establish_connection(data):
  try:
    connection = sqlite3.connect(data)
    cur = connection.cursor()
  except Error as e:
    print(e)
  return connection, cur

def destroy_connection(connection):
  try:
    connection.commit()
    connection.close()
  except Error as e:
    print(e)
  return

def set_database(connection, cursor, df_stock):
  try:
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS financial_data(
      symbol TEXT,
      date TEXT,
      open_price REAL,
      close_price REAL,
      volume INTEGER,
      PRIMARY KEY (symbol, date)
    )''')

    print("Here are the contents of the table: \n1: symbol. \n2: date. \n3: open_price. \n4: close_price. \n5: volume.")

    cursor.executemany("INSERT OR REPLACE INTO financial_data(symbol, date, open_price, close_price, volume) VALUES (?, ?, ?, ?, ?);", df_stock.values)
  except sqlite3.Error() as e:
    print(e, " occured")

  destroy_connection(connection)
  return

def get_database():
  try:
    connection, cursor = establish_connection('financial_data.db')
      
    # storing the data in a list
    data_list = cursor.execute("SELECT * FROM financial_data")
    names = list(map(lambda x: x[0], cursor.description))
    print(names[0] + '\t ' + names[1] + '\t ' + names[2] + '\t ' + names[3] + '\t ' + names[4])
    print('------' + '\t ----' + '\t ----------' + '\t -----------' + '\t ------')
    for item in data_list:
      print(item[0] + ' | ' + item[1] + ' | ' + str(item[2]) + ' \t| ' + str(item[3]) + ' \t| ' + str(item[4]))   
          
  except sqlite3.OperationalError:
    print("No such table: financial_data")

  destroy_connection(connection)
  return
