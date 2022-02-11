from bs4 import BeautifulSoup
import sqlite3
from utils import get_soup

base_url = "https://csgostash.com/skin/"
db = sqlite3.connect('skinbase.db')


def get_full_name(soup: BeautifulSoup):
    name = soup.find('div', class_='well result-box nomargin').find('h2').text
    return name


def get_rarity(soup: BeautifulSoup):
    rarity = soup.find('span', class_='rarity-search-icon').parent.text.split()[0]
    return rarity


def get_collection(soup: BeautifulSoup):
    collection = soup.find('div', class_='skin-details-collection-container').find_all('p',class_='collection-text-label').pop().text
    return collection


def get_skin(stash_id: int):
    soup = get_soup(stash_id)
    name = get_full_name(soup)
    weapon, name = name.split(' | ')
    rarity = get_rarity(soup)
    print(name, rarity)
    return stash_id, weapon, name, rarity


def create_db():
    with open('skinbase.sql') as sql_file:
        sql_script = sql_file.read()
    db.cursor().executescript(sql_script)
    db.commit()
    db.close()
