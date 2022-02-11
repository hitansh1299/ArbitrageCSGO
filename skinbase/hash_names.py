from utils import get_soup, db, conditions
import re
from urllib.parse import unquote
from bs4 import BeautifulSoup


def get_hash_name(soup: BeautifulSoup):
    table = soup.find('div', id='prices')
    rows = table.find_all('div', class_='btn-group-sm')[1:]
    hash_names = {}
    for row in rows:
        wear_name = row.find_all('span', class_='pull-left')
        wear = ' '.join([x.text.replace('\n', '') for x in wear_name])
        link = str(row.find('a').get('href'))
        hash_name = unquote(link.split('/')[-1])
        hash_names[wear] = hash_name
    print('steam: ', hash_names)
    return hash_names


def update_hash_names(stash_id: int):
    soup = get_soup(stash_id)
    hash_names = get_hash_name(soup)
    for i in hash_names.keys():
        db.cursor().execute('UPDATE Hash_Names SET hash_name = ? WHERE stash_id = ? AND condition_id = ?', (stash_id, conditions[i], hash_names[i]))


def update_all_hash_names():
    ids = [x[0] for x in db.execute('SELECT CSGOStash_id FROM Skins').fetchall()]
    #db.execute('DELETE FROM Hash_Names')
    for i,id in enumerate(ids):
        update_hash_names(id)

        if i % 20 == 0:
            db.commit()
    db.commit()


if __name__ == '__main__':
    update_all_hash_names()