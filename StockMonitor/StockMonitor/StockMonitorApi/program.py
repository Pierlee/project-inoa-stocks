from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS 
import pyodbc

app = Flask(__name__)
CORS(app)

cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for PostgreSQL};Server=localhost;Port=5432;Database=StockMonitor;User ID=postgres;Password=admin;String Types=Unicode') # connect into database
cursor = cnxn.cursor()

@app.route('/tracked-stocks-list', methods = ['GET'])
def tracked_stocks_list():
    rows = cursor.execute('SELECT stockname, creationdate, minvalue, maxvalue FROM public.TrackedStocks;').fetchall() # get all tacked stocks
    stocks = []
    if rows is None: 
      return stocks
    
    for row in rows: #format in array
      stock = {}
      stock['symbol'] = row[0]
      stock['creationDate'] = row[1]
      stock['minValue'] = row[2]
      stock['maxValue'] = row[3]
      stocks.append(stock)
    
    return stocks

@app.route('/stock-history', methods = ['GET'])
def stock_history():
    symbol = request.args.get('symbol')
    if symbol is None: 
      return (jsonify(success=False, Message="No symbol given!"))

    query = 'SELECT stockname, "timestamp", currentvalue FROM public.stockshistory WHERE stockName = ?;'
    rows = cursor.execute(query, (symbol.upper(),)).fetchall()

    stocks = []
    if rows is None: return stocks
    
    stock = {}
    for row in rows: #format in array
      stock['symbol'] = row[0]
      stock['timestamp'] = row[1]
      stock['currentValue'] = row[2]
      stocks.append(stock)
    
    return stocks

@app.route('/tracked-stocks-delete', methods = ['DELETE'])
def tracked_stocks_delete():
    symbol = request.args.get('symbol')
    if symbol is None: 
      return (jsonify(success=False, Message="No symbol given!"))
    
    query = 'SELECT count(1) as cnt FROM public.TrackedStocks WHERE stockName = ?;'
    stock = cursor.execute(query, (symbol.upper(),)).fetchval()
    
    if stock == 0: 
      return (jsonify(success=False, Message="No stock found!"))
    
    cursor.execute(f"DELETE FROM public.stockshistory WHERE stockname = '{symbol.upper()}'").commit()
    cursor.execute(f"DELETE FROM public.trackedstocks WHERE stockname = '{symbol.upper()}'").commit()
    
    return jsonify(success=True)


@app.route('/tracked-stocks-save', methods = ['POST'])
def tracked_stocks_save():
    symbol = request.json.get('symbol')
    minvalue = request.json.get('minValue')
    maxvalue = request.json.get('maxValue')

    cursor.execute(f'INSERT INTO public.trackedstocks(\
                  stockname, creationdate, minvalue, maxvalue)\
                  VALUES (\'{symbol.upper()}\', CURRENT_TIMESTAMP, {minvalue}, {maxvalue});').commit()

    return jsonify(success=True)

if __name__ == '__main__':
    app.run()
