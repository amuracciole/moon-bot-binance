import requests
import config

## https://www.youtube.com/watch?v=M9IGRWFX_1w&ab_channel=BaoLuThe

def send_telegram_msg(side, date, quantity, earn):
    token = config.TELEGRAM_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID
    if(side=="BUY"):
        text= "(" + str(date) + ") --> " + str(side) + "\n----------------------\n" + str(quantity) + " BTC"
    elif(side=="SELL"):
            text= "(" + str(date) + ") --> " + str(side) + "\n-----------------------\n" + str(quantity) + " BTC \n\nEARN: " + str(earn) + " %"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())
