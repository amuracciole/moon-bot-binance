#!/usr/bin/env python3
import requests
import config

# https://www.youtube.com/watch?v=M9IGRWFX_1w&ab_channel=BaoLuThe

def send_telegram_msg(side, date, quantity, earn):
    #token = config.TELEGRAM_TOKEN
    token='5476845537:AAEQ9DEp-B3LnjZ0nbAiBd2chu_AsI4kvio'
    #chat_id = config.TELEGRAM_CHAT_ID
    chat_id='1538349259'
    if(side=="BUY"):
        text= "(" + str(date) + ") --> " + str(side) + "\n----------------------\n" + str(quantity) + " BTC"
    elif(side=="SELL"):
        text= "(" + str(date) + ") --> " + str(side) + "\n-----------------------\n" + str(quantity) + " BTC \n\nEARN: " + str(earn) + " %"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())

