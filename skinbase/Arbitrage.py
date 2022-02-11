from utils import db


def get_arbitrage_sell_prices():
    skins = db.execute('SELECT * FROM Hash_Names NATURAL JOIN Prices WHERE bitskins_buy_order_price IS NOT NULL;').fetchall()
    skins = list(filter(lambda x: x[5] != -1 and x[3] != -1, skins))
    skins = [x + (str(round(((x[5] - x[3]) / x[3]) * 100, 2)) + '%',) for x in skins] # percentage gain over buy-order(x[3]) prices
    skins.sort(key=lambda x: float(x[-1][:-1]), reverse=True)
    skins = list(filter(lambda x: x[3] > 100, skins))
    print(*skins, sep='\n')


def get_arbitrage_buy_prices():
    skins = db.execute('SELECT * FROM Hash_Names NATURAL JOIN Prices WHERE bitskins_buy_order_price IS NOT NULL AND  NOT Bitskins_Price = 0;').fetchall()
    skins = list(filter(lambda x: x[5] != -1 and x[4] != -1, skins))
    skins = [x + (str(round(((x[3] - x[4]) / x[4]) * 100, 2)) + '%',) for x in skins]
    skins.sort(key=lambda x: float(x[-1][:-1]), reverse=True)
    skins = list(filter(lambda x: 400 < x[3] < 750, skins))
    print(*skins, sep='\n')


if __name__ == '__main__':
    print('BUY: ')
    get_arbitrage_buy_prices()
    print('\n\n\n========================================================================================\n\n')
    print('SELL: ')
    get_arbitrage_sell_prices()