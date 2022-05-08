import os

import ccxt
from dotenv import load_dotenv

from file_loader import FileLoader
from grid import Grid


def grid_bot(name):
    print('Load in environment variables.')
    load_dotenv()
    APIKEY = os.getenv('APIKEY')
    SECRET = os.getenv('SECRET')
    UID = os.getenv('UID')
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')
    print('Load and test the grid.')
    # Create a new grid, load dummy data, and then test against data
    fl = FileLoader()
    g = Grid(10, 0.155, 0.1775, 50, 4)  # Intervals, Min Price, Max Price, Amount per Interval
    # g.set_data(fl.load_dummy_data('data1.csv'))
    data = fl.load_data('ndax_data.json')
    g.set_data(data)
    g.simulator()

    # Load NDAX API access
    ndax = ccxt.ndax({
        'apiKey': APIKEY,
        'secret': SECRET,
        'uid': UID,
        'login': LOGIN,
        'password': PASSWORD
    })

    currencies = ndax.fetch_currencies()
    # print(currencies)

    markets = ndax.fetch_markets()
    # print(markets)

    ticker = ndax.fetch_ticker('DOGE/CAD')
    # print(ticker)

    ohlcv = ndax.fetch_ohlcv('DOGE/CAD', timeframe='1m', since=1651948200)
    # fl.save_data(ohlcv, 'ndax_data.json')

    balance = ndax.fetch_balance()
    # print(balance)

    fees = ndax.fetch_fees()
    # print(fees)

    deposits = ndax.fetch_deposits()
    # print(deposits)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    grid_bot('TEST')
