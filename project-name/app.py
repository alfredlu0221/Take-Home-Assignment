from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

from datetime import datetime
import math
import json
import sqlite3

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

@app.route('/api/financial_data')
def get_financial_data():
  try:
    connection, cursor = establish_connection('financial_data.db')

    start_date = request.args.get('start_date', default = '1970-01-01', type = str)
    end_date = request.args.get('end_date', default = datetime.today().strftime('%Y-%m-%d'), type = str)
    symbol = request.args.get('symbol', default = None, type = str)
    limit = request.args.get('limit', default = 5, type = int)
    page = request.args.get('page', default = 1, type = int)

    # storing the data in a list
    if symbol is None:
      rows_data = cursor.execute("SELECT * FROM financial_data")
    else:
      rows_data = cursor.execute("SELECT * FROM financial_data WHERE symbol=? AND date BETWEEN ? AND ?", (symbol, start_date, end_date, ))

    results = {}
    result = []
    if rows_data:
      column_names = list(map(lambda x: x[0], cursor.description))
      for row in rows_data:
        result.append( dict(zip(column_names, row)) )

    results['data'] = result[(limit*(page-1)):limit*page]
    results.setdefault('pagination', {}).setdefault('count',len(result))
    results.setdefault('pagination', {}).setdefault('page',page)
    results.setdefault('pagination', {}).setdefault('limit',limit)
    results.setdefault('pagination', {}).setdefault('pages',math.ceil(len(result)/limit))
    results['info'] = {'error': ''}
    
  except sqlite3.OperationalError:
    print("No such table: financial_data")

  destroy_connection(connection)
  return json.dumps(results, indent=4)

@app.route('/api/statistics')
def get_statistics():
  try:
    connection, cursor = establish_connection('financial_data.db')

    start_date = request.args.get('start_date', default = None, type = str)
    end_date = request.args.get('end_date', default = None, type = str)
    symbol = request.args.get('symbol', default = None, type = str)

    # storing the data in a list
    rows_data = {}
    if start_date is None or end_date is None or symbol is None:
      print("All parameters are required: financial_data")
    else:
      cursor.execute("SELECT * FROM financial_data WHERE symbol=? AND date BETWEEN ? AND ?", (symbol, start_date, end_date, ))
      rows_data = cursor.fetchall()

    results = {}
    average_daily_open_price = 0
    average_daily_close_price = 0
    average_daily_volume = 0

    if rows_data:
      for row in rows_data:
        average_daily_open_price += row[2]
        average_daily_close_price += row[3]
        average_daily_volume += row[4]
      average_daily_open_price /= len(rows_data)
      average_daily_close_price /= len(rows_data)
      average_daily_volume /= len(rows_data)

    results.setdefault('data', {}).setdefault('start_date',start_date)
    results.setdefault('data', {}).setdefault('end_date',end_date)
    results.setdefault('data', {}).setdefault('symbol',symbol)
    results.setdefault('data', {}).setdefault('average_daily_open_price',average_daily_open_price)
    results.setdefault('data', {}).setdefault('average_daily_close_price',average_daily_close_price)
    results.setdefault('data', {}).setdefault('average_daily_volume',average_daily_volume)
    results['info'] = {'error': ''}
    
  except sqlite3.OperationalError:
    print("No such table: financial_data")

  destroy_connection(connection)
  return json.dumps(results, indent=4)
