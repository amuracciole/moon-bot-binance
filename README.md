# BinanceBot
This is a bot programed in Python and the idea is to optimize SELL and BUY orders taking into account the moon state:
- FULL MOON: Buy BTC
- NEW MOON: Sell BTC

![Moon trading](https://github.com/amuracciole/moon_bot_binance/blob/main/picture.png)

**ALERT!: This is an academic task and NOT AN INVST ADVISE**

## Comment 1
Plese add you own API_KEY and API_SECRET in config.py file.

## Comment 2
You must include the following line in you crontab file to run the script every day at 4:00 AM (You can schedule as you wish)

0 4 * * * python3 (project path)

## Comment 3
This script will never buy or sell BTC because only run "test_order". In case you want to work with real operations, please comment test_order lines and delete "#" before "order_market_sell" and "order_market_buy" lines