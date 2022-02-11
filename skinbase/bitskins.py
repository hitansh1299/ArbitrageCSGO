import requests
from requests_futures.sessions import FuturesSession
import pyotp
import sqlite3
from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import unquote, quote

API_KEY = '12667e1e-68f5-4dad-89ec-d0e4a2493f0b'
secret = 'JUSR34EFHHLGH7QE'
token = str(pyotp.TOTP(secret).now())
db = sqlite3.connect('skinbase.db')
exchange_rate = round(float(requests.get('https://v6.exchangerate-api.com/v6/d65d468f87598767cc2fc110/latest/USD').json()['conversion_rates']['INR']), 2)


def get_steam_buy_order_price(hash_name: str):
    url = f'http://steamcommunity.com/market/listings/730/{hash_name}'

    print(url)
    res = requests.get(url)
    print(res.text)


def update_bitskins_buy_order_price():
    buy_orders = get_buy_orders()
    hash_names = db.execute("SELECT skin_id, condition_id, hash_name FROM Hash_Names NATURAL JOIN Prices WHERE NOT hash_name = 'None'").fetchall()
    for name in hash_names:
        db.execute('UPDATE Prices SET bitskins_buy_order_price = ? WHERE skin_id = ? AND condition_id = ?', (buy_orders.get(name[2], -1), name[0], name[1]))
    db.commit()


def get_buy_orders():
    json = requests.get(f'https://bitskins.com/api/v1/summarize_buy_orders/?api_key=12667e1e-68f5-4dad-89ec-d0e4a2493f0b&app_id=730&code={token}').json()
    items = json['data']['items']
    buy_orders = {}
    for i in items:
        buy_orders[i[0]] = round(float(i[1]['max_price'])*exchange_rate, 2)
    for b in buy_orders:
        print(b, ':', buy_orders[b])
    return buy_orders


if __name__ == '__main__':
    get_steam_buy_order_price('StatTrak™ M4A4 | Evil Daimyo (Minimal Wear)')
