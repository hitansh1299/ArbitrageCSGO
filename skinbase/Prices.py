from bs4 import BeautifulSoup
from utils import conditions, db, get_soup
from bitskins import update_bitskins_buy_order_price
import re


def get_steam_prices(soup: BeautifulSoup):
    table = soup.find('div', id='prices')
    rows = table.find_all('div', class_='btn-group-sm')[1:]
    wears = {}
    for row in rows:
        wear_name = row.find_all('span', class_='pull-left')
        wear = ' '.join([x.text.replace('\n', '') for x in wear_name])
        price = re.sub('[^0-9]', "", row.find('span', class_='pull-right').text)
        wears[wear] = -1 if price == '' else float(price)
    print('steam: ', wears)
    return wears


def get_bitskins_prices(soup: BeautifulSoup):
    table = soup.find('div', id='bitskins')
    rows = table.find_all('div', class_='btn-group-sm')[1:]
    wears = {}
    for row in rows:
        wear_name = row.find_all('span', class_='pull-left')
        wear = ' '.join([x.text.replace('\n', '') for x in wear_name])
        price = re.sub('[^0-9]', "", row.find('span', class_='pull-right').text)
        wears[wear] = -1 if price == '' else float(price)
    print('bitskins:', wears)
    return wears


def get_prices(soup: BeautifulSoup):
    return get_steam_prices(soup), get_bitskins_prices(soup)


def update_prices(stash_id: int):
    soup = get_soup(stash_id)
    steam, bitskins = get_prices(soup)
    for i in steam.keys():
        print(i)
        db.cursor().execute("UPDATE Prices SET Steam_price = ?, Bitskins_price = ? WHERE Skin_ID = ? AND Condition_ID = ?", (steam[i], bitskins[i], stash_id, conditions[i]))


def update_all_prices():
    #db.cursor().execute("DELETE FROM Prices")
    ids = [x[0] for x in db.cursor().execute('SELECT CSGOStash_ID FROM Skins').fetchall()]
    for id in ids:
        update_prices(id)
        db.commit()


if __name__ == '__main__':
    #update_all_prices()
    update_bitskins_buy_order_price()


