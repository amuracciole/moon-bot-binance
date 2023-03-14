#!/usr/bin/env python3
import requests
import config

# https://www.youtube.com/watch?v=M9IGRWFX_1w&ab_channel=BaoLuThe

def send_telegram_msg(code, date, quantity, earn):
    #token = config.TELEGRAM_TOKEN
    token='5476845537:AAEQ9DEp-B3LnjZ0nbAiBd2chu_AsI4kvio'
    #chat_id = config.TELEGRAM_CHAT_ID
    chat_id='1538349259'
    if(code=="BUY"):
        text= "(" + str(date) + ") --> " + str(code) + "\n----------------------\n" + str(quantity) + " BTC"
    elif(code=="SELL"):
        if float(earn) > 0:
            emoji = "🟢"
        elif float(earn) < 0:
            emoji = "🔴"
        else:
            emoji = "🟡"
        text= "(" + str(date) + ") --> " + str(code) + "\n-----------------------\n" + str(quantity) + " BTC \n\n" + emoji + " EARN: " + str(earn) + " %"
    elif(code=="DAY"):
        text= "Script run"
    elif(code=="BINANCE_ERROR"):
        text= "❗ The program could not be executed. Check that the created API still exists or that the secure IPs include your current public IP."
    elif(code=="TEST"):
        text = code
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())

