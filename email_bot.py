#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
import config

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