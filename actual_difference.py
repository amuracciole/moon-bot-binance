#!/usr/bin/env python3

from symtable import Symbol
from binance.client import Client
import config
from os import system

client = Client(config.API_KEY, config.API_SECRET)
###################
##   FUNCTIONS   ##
###################

def get_current_price(pair):
  current_prices = client.get_all_tickers()
  for coin in current_prices:
      if(coin["symbol"] == pair):
         return(coin["price"])

def calculate_diffenrence(last_buy_price, last_sell_price):
    result = round((float(last_sell_price)-float(last_buy_price))*100/float(last_buy_price),2)
    return(result)

def read_last_value(file):
    with open(file, 'r') as f:
        for line in f:
            pass
        last_line = line
    return(last_line)

def read_last_history_value(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines[-2]



###################
##    PROGRAM    ##
###################
system("clear")
sell_flag = read_last_value(config.FLAG_PATH)
last_buy_price=str(read_last_value(config.BUY_PATH))
current_price=str(get_current_price("BTCUSDT"))
diff=calculate_diffenrence(last_buy_price, current_price)
if(sell_flag == "1\n"):
    btc_bought=read_last_value(config.HISTORIC_PATH)[27:-26]
    used_usdt = float(str(btc_bought))*float(str(last_buy_price))
    print("\n--------------------")
    print("LAST BUY: " + str(last_buy_price[:-7])+ " USDT")
    print("CURRENT PRICE: " + str(current_price[:-6]) + " USDT")
    print("DIFFERENCE: " + str(float(current_price) - float(last_buy_price[:-1]))[:-12] + " USDT")
    print("\nEARN IF YOU SELL RIGHT NOW: " + str(diff)+ "%")
    print("EARNS IN USDT: " + str(float(str(btc_bought))*float(str(current_price))-used_usdt)[:-16] + " USDT")
    print("--------------------\n")
else:
    last_sell_price=str(read_last_value(config.SELL_PATH))
    last_trade=read_last_history_value(config.HISTORIC_PATH)
    start = last_trade.find("TRADE: ") + len("TRADE: ")
    print("LAST SELL: " + str(last_sell_price[:-7])+ " USDT")
    print("CURRENT PRICE: " + str(current_price[:-6]) + " USDT")
    print("You already sold BTC and result was: " + str(last_trade[start:-1]))
    print("If you had not sold and are selling now the result would have been: " + str(diff)+ "%")
    