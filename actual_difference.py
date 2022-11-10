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


###################
##    PROGRAM    ##
###################
system("clear")
sell_flag = read_last_value(config.FLAG_PATH)
last_buy_price=str(read_last_value(config.BUY_PATH))
current_price=str(get_current_price("BTCBUSD"))
diff=calculate_diffenrence(last_buy_price, current_price)
btc_bought=read_last_value(config.HISTORIC_PATH)[27:-26]
used_busd = float(str(btc_bought))*float(str(last_buy_price))
if(sell_flag == "1\n"):
    print("\n--------------------")
    print("LAST BUY: " + str(last_buy_price[:-7])+ " BUSD")
    print("CURRENT PRICE: " + str(current_price[:-6]) + " BUSD")
    print("DIFFERENCE: " + str(float(current_price) - float(last_buy_price[:-1]))[:-12] + " BUSD")
    print("\nEARN IF YOU SELL RIGHT NOW: " + str(diff)+ "%")
    print("EARNS IN BUSD: " + str(float(str(btc_bought))*float(str(current_price))-used_busd)[:-16] + " BUSD")
    print("--------------------\n")
else:
    print("YOU ALREADY SOLD BTC. WAIT TO THE NEXT ROUND")