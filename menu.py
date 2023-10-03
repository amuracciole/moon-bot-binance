import os
import time
import config
from binance.client import Client
import dates
from telegram_bot import *
from email_bot import *
from datetime import date, datetime

client = Client(config.API_KEY, config.API_SECRET)

def menu():
    print("1 - Check last BUY")
    print("2 - Check last SELL")
    print("3 - Actual difference")
    print("4 - Get current BTC/USD price")
    print("5 - Check logs list")
    print("6 - See history file")
    print("7 - See difference file")
    print("8 - Next SELL/BUY day")
    print("9 - Test Telegram message")
    print("10 - Test email")
    print("0 - EXIT")


def read_last_value(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines[-1]

def get_current_price(pair):
  current_prices = client.get_all_tickers()
  for coin in current_prices:
      if(coin["symbol"] == pair):
         return(coin["price"])

flag = True    
while flag:
    os.system("clear")
    menu()
    option = input("\nYour option: ")

    if option == "1":
        print ("LAST BUY: " + str(read_last_value(config.BUY_PATH))[:-7] + " USD")
        input("\nPress enter to continue")
    elif option == "2":
        print ("LAST SELL: " + str(read_last_value(config.SELL_PATH))[:-7] + " USD")
        input("\nPress enter to continue")
    elif option == "3":
        exec(open("./actual_difference.py").read())
        input("\nPress enter to continue")
    elif option == "4":
        current_price=str(get_current_price("BTCUSDT"))
        print("CURRENT PRICE: " + str(current_price[:-6]) + " USDT")
        input("\nPress enter to continue")
    elif option == "5":
        with open("logs.txt") as f:
            print(f.read())
        input("\nPress enter to continue")
    elif option == "6":
        with open("historic.txt") as f:
            print(f.read())
        input("\nPress enter to continue")
    elif option == "7":
        with open("difference.txt") as f:
            print(f.read())
        input("\nPress enter to continue")
    elif option == "8":
        today = str(date.today())
        fullmoon=[]
        newmoon=[]
        
        for x in dates.full_moon:
            if x > today:
                fullmoon.append(x)
        
        for x in dates.new_moon:
            if x > today:
                newmoon.append(x)

        date1 = datetime.strptime(today, '%Y-%m-%d')
        date2 = datetime.strptime(fullmoon[0], '%Y-%m-%d')
        date3 = datetime.strptime(newmoon[0], '%Y-%m-%d')
        print("NEXT FULL MOON (BUY): " + str(fullmoon[0]) + " -> In " + str(date2 - date1)[:-9])
        print("NEXT NEW MOON (SELL): " + str(newmoon[0]) + " -> In " + str(date3 - date1)[:-9])
        input("\nPress enter to continue")
    elif option == "9":
        today = str(date.today())
        send_telegram_msg("TEST", today, "null", "null")
    elif option == "10":
        today = str(date.today())
        send_email("TEST", today, "0", "0")
    elif option == "0":
        os.system("clear")
        flag = False
    else:
        print("Wrong option. Try agin.")
        time.sleep(2)