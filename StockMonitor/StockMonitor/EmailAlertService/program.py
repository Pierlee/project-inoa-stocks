import pyodbc
import time
from types import SimpleNamespace
import smtplib, ssl
import json
import os
from email.message import EmailMessage

def send_email(emailSettings, message, subject):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject

    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP(emailSettings['host'], emailSettings['port']) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(emailSettings['login'], emailSettings['password'])
        server.sendmail(emailSettings['login'], emailSettings['to'], msg.as_string())

with open(f'{os.path.dirname(os.path.realpath(__file__))}/settings.json', "r") as jsonfile:
    emailSettings = json.load(jsonfile)

sleepTime = 1*60 # 1 minute

cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for PostgreSQL};Server=localhost;Port=5432;Database=StockMonitor;User ID=postgres;Password=admin;String Types=Unicode') # connect into database
cursor = cnxn.cursor()
lastValueBySymbol = {}
while True:
  rows = cursor.execute(f'SELECT DISTINCT ON (sh.StockName)\
                            sh.StockName,\
                            sh.Timestamp,\
                            sh.CurrentValue,\
                        	ts.MinValue,\
	                        ts.MaxValue\
                        FROM public.StocksHistory sh\
                        INNER JOIN public.TrackedStocks ts ON ts.StockName = ts.StockName\
                        ORDER BY sh.StockName, sh.Timestamp DESC;').fetchall() # get all stocks history

  if rows is None: # if don't have tracked history wait to continue
    time.sleep(sleepTime)
    continue
  
  historical = []
  history = SimpleNamespace()
  for row in rows: #format in array object
      history.symbol = row[0]
      history.timestamp = row[1]
      history.currentValue = row[2]
      history.MinValue = row[3]
      history.MaxValue = row[4]
      historical.append(history)

  for stock in historical:
    if stock.symbol not in lastValueBySymbol:
        lastValueBySymbol[stock.symbol] = [history.currentValue, history.MinValue, history.MaxValue]
    elif lastValueBySymbol[stock.symbol][0] == history.currentValue and lastValueBySymbol[stock.symbol][1] == history.MinValue and lastValueBySymbol[stock.symbol][2] == history.MaxValue:
       time.sleep(sleepTime)
       continue

    if lastValueBySymbol[stock.symbol][0] <= history.MinValue:
       send_email(emailSettings, f"Sugestão de compra: {stock.symbol} está abaixo do valor mínimo.", 'Sugestão de compra') #TODO AJUSTAR MENSAGENS

    if lastValueBySymbol[stock.symbol][0] >= history.MaxValue:
       send_email(emailSettings, f"Sugestão de venda: {stock.symbol} está acima do valor máximo.", 'Sugestão de venda') #TODO AJUSTAR MENSAGENS

    lastValueBySymbol[stock.symbol] = [history.currentValue, history.MinValue, history.MaxValue]
    time.sleep(sleepTime)


