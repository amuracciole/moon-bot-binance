#!/usr/bin/env python3

from symtable import Symbol
from binance.client import Client
import config
import dates
from datetime import date
import smtplib
from email.mime.text import MIMEText

client = Client(config.API_KEY, config.API_SECRET)

###################
##   FUNCTIONS   ##
###################

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

def add_line_in_file(text, file):
    if(file=="historic"):
        file_object = open(config.HISTORIC_PATH, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()
        #print("\n  DATE        OPERATION       BTC              PRICE        ")
        #print(str(text))
    elif(file=="buy"):
        file_object = open(config.BUY_PATH, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()
        #print(str(text))
    elif(file=="sell"):
        file_object = open(config.SELL_PATH, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()
        #print(str(text))

def add_log(text):
    file_object = open(config.LOGS_PATH, 'a')
    file_object.write(str(text) + "\n")
    file_object.close()

def send_email(side, date, quantity, earn):
    correo_origen = config.EMAIL_FROM
    clave = config.EMAIL_PASS
    correo_destino =config.EMAIL_TO

    msg = MIMEText("(" + str(date) + ") -  BOT " + str(side) + " - " +  str(quantity) + " BTC")
    if (side=="BUY"):
        msg['Subject'] = str(date) + ' --> BTC BOT Operation'
    elif (side=="SELL"):
        msg['Subject'] = str(date) + ' --> BTC BOT Operation --> (' + str(earn) + ' %)' 
    msg['From'] = correo_origen
    msg['To'] = correo_destino

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(correo_origen,clave)
    server.sendmail(correo_origen,correo_destino,msg.as_string())

    server.quit()

def calculate_diffenrence(last_buy_price, last_sell_price):
    result = round((float(last_sell_price)-float(last_buy_price))*100/float(last_buy_price),2)
    return(result)

def read_last_buy_price(file):
    with open(file, 'r') as f:
        for line in f:
            pass
        last_line = line
    return(last_line)


###################
##    PROGRAM    ##
###################

#Current date
today = str(date.today())
print("\n**********************\n")
print("DATE:", today)
add_log(today)

#Get balance (before operation)
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
        current_price=str(get_current_price("BTCBUSD"))
        add_line_in_file(str(today) + "      " + "SELL" + "       " + str(qnt_sell) + "             " + current_price,"historic")
        add_line_in_file(current_price,"sell")
        last_buy_price=str(read_last_buy_price(config.BUY_PATH))
        last_sell_price=current_price
        diff=calculate_diffenrence(last_buy_price, last_sell_price)
        add_line_in_file("EARNS IN THE LAST TRADE: " + str(diff) + " %", "historic")
        send_email("SELL", today, str(qnt_sell), str(diff))

#BUY
for x in dates.full_moon:
    if(today==x):
        qnt_buy = str(balances[1]/float(get_current_price("BTCBUSD")))[0:7]
        buy_order = client.create_test_order(symbol="BTCBUSD", side="BUY", type="MARKET", quantity=qnt_buy)
        #buy_order = client.create_order(symbol="BTCBUSD", side="BUY", type="MARKET", quantity=qnt_buy)
        add_line_in_file(str(today) + "      " + "BUY" + "       " + str(get_balance()[0]) + "             " + str(get_current_price("BTCBUSD")),"historic")
        add_line_in_file(str(get_current_price("BTCBUSD")),"buy")
        send_email("BUY", today, str(get_balance()[0]), 0)

#Get balances (after)
print("\nBALANCE (AFTER):")
balances_after = get_balance()
print("BTC: " + str(balances_after[0]))
print("BUSD: " + str(balances_after[1]))
print("\n**********************\n")