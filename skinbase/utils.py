import sqlite3
import requests
from CustomExceptions import *
from bs4 import BeautifulSoup
db = sqlite3.connect('skinbase.db')

base_url = "https://csgostash.com/skin/"

conditions = {
    'Factory New': 0,
    'Minimal Wear': 1,
    'Field-Tested': 2,
    'Well-Worn': 3,
    'Battle-Scarred': 4,
    'StatTrak Factory New': 5,
    'StatTrak Minimal Wear': 6,
    'StatTrak Field-Tested': 7,
    'StatTrak Well-Worn': 8,
    'StatTrak Battle-Scarred': 9,
    'Souvenir Factory New': 10,
    'Souvenir Minimal Wear': 11,
    'Souvenir Field-Tested': 12,
    'Souvenir Well-Worn': 13,
    'Souvenir Battle-Scarred': 14,
    'Vanilla':15,
    'StatTrak Vanilla':16
}


def get_soup(stash_id: int) -> BeautifulSoup:
    req = requests.get(base_url+str(stash_id))
    if req.status_code != 200:
            raise NoSuchSkinException
    return BeautifulSoup(req.content, 'html.parser')