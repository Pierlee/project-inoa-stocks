import pyodbc 
import requests
import time
import json

sleepTime = 5*60 # 5 minute

cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for PostgreSQL};Server=localhost;Port=5432;Database=StockMonitor;User ID=postgres;Password=admin;String Types=Unicode') # connect into database
cursor = cnxn.cursor()
while True:
  rows = cursor.execute('SELECT stockname FROM public.TrackedStocks;').fetchall() # get all tacked stocks

  if rows is None: # if don't have tracked stocks wait to continue
    time.sleep(sleepTime)
    continue

  symbols = []
  for row in rows: #format in array
      symbols.append(row[0])

  response = requests.get(f'https://api.hgbrasil.com/finance/stock_price?key=5348bce0&symbol={",".join(symbols)}') # api request current stock price
  if response.ok is False: # if the status is not ok, print error, wait and continue
    print(response.status_code)
    time.sleep(sleepTime)
    continue

  content = json.loads(response.content.decode('utf-8')) # load response
  for symbol in symbols: # for each symbol insert into database the current value
     currentStock = content['results'][symbol.upper()]
     cursor.execute(f'INSERT INTO public.stockshistory(stockname, "timestamp", currentvalue) VALUES (\'{symbol.upper()}\', CURRENT_TIMESTAMP, {currentStock['price']});').commit()
  time.sleep(sleepTime)