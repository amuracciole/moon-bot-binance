#!/usr/bin/env python3

from symtable import Symbol
from binance.client import Client
import config
import dates
from datetime import date
import smtplib
from email.mime.text import MIMEText

client = Client(config.API_KEY, config.API_SECRET)

def get_balance():
    btc_balance = client.get_asset_balance(asset='BTC')
    busd_balance = client.get_asset_balance(asset='BUSD')
    #Convert balances to float
    btc_float = float(btc_balance["free"])
    busd_float = float(busd_balance["free"])
    return btc_float, busd_float

def get_current_price(pair):
  current_prices = client.get_all_tickers()
  for coin in current_prices:
      if(coin["symbol"] == pair):
         return(coin["price"])

def add_line_in_file(text):
    file_object = open(config.HISTORIC_PATH, 'a')
    file_object.write(str(text) + "\n")
    file_object.close()
    print("\n  DATE        OPERATION       BTC              PRICE        ")
    print(str(text))

def add_log(text):
    file_object = open(config.LOGS_PATH, 'a')
    file_object.write(str(text) + "\n")
    file_object.close()

def send_email(side, date, quantity):
    correo_origen = config.EMAIL_FROM
    clave = config.EMAIL_PASS
    correo_destino =config.EMAIL_TO

    if (side == "SELL"):
      msg = MIMEText("(" + str(date) + ") -  BOT " + str(side) + " " +  str(quantity) +  " BTC")
    elif (side == "BUY"):
      msg = MIMEText("(" + str(date) + ") -  BOT " + str(side) + " " +  str(quantity) + " BTC")
    msg['Subject'] = str(date) + ' --> BTC BOT Operation'
    msg['From'] = correo_origen
    msg['To'] = correo_destino

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(correo_origen,clave)
    server.sendmail(correo_origen,correo_destino,msg.as_string())

    server.quit()

#Current date
today = str(date.today())
print("\n**********************\n")
print("DATE:", today)
add_log(today)

#Get balance (before)
print("\nBALANCE (BEFORE):")
balances = get_balance()
print("BTC: " + str(balances[0]))
print("BUSD: " + str(balances[1]))

#SELL
for x in dates.new_moon:
    if(today==x):
        qnt_sell=str(balances[0])[0:7]
        sell_order = client.create_test_order(symbol="BTCBUSD", side="SELL", type="MARKET", quantity=qnt_sell)
        #sell_order = client.create_order(symbol="BTCBUSD", side="SELL", type="MARKET", quantity=qnt_sell)
        add_line_in_file(str(today) + "      " + "SELL" + "       " + str(qnt_sell) + "       " + str(get_current_price("BTCBUSD")))
        send_email("SELL", today, str(qnt_sell))

#BUY
for x in dates.full_moon:
    if(today==x):
        qnt_buy = str(balances[1]/float(get_current_price("BTCBUSD")))[0:7]
        buy_order = client.create_test_order(symbol="BTCBUSD", side="BUY", type="MARKET", quantity=qnt_buy)
        #buy_order = client.create_order(symbol="BTCBUSD", side="BUY", type="MARKET", quantity=qnt_buy)
        add_line_in_file(str(today) + "      " + "BUY" + "       " + str(get_balance()[0]) + "       " + str(get_current_price("BTCBUSD")))
        send_email("BUY", today, str(get_balance()[0]))

#Get balances (after)
print("\nBALANCE (AFTER):")
balances_after = get_balance()
print("BTC: " + str(balances_after[0]))
print("BUSD: " + str(balances_after[1]))
print("\n**********************\n")