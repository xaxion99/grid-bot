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
    # g = Grid(50, 0.155, 0.177, 1, 4)  # Example of bad situation
    g = Grid(18, 0.155, 0.177, 100, 4)  # Intervals, Min Price, Max Price, Amount per Interval
    # g.set_data(fl.load_dummy_data('data/data1.csv'))
    data = fl.load_data('data/ndax_data_08_May_22.json')
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

    # OHLC(V) Candle Retriever
    # ohlcv = ndax.fetch_ohlcv('DOGE/CAD', timeframe='1m', since=1651966200)  # since= uses UNIX time
    # fl.save_data(ohlcv, 'data/ndax_data_08_May_22.json')
    # Check basic stats of the retrieved data
    # d = fl.load_data('data/ndax_data_08_May_22.json')
    # print(f'Min: {min(d.values())}')
    # print(f'Mid: {(min(d.values()) + max(d.values())) / 2}')
    # print(f'Max: {max(d.values())}')

    # currencies = ndax.fetch_currencies()
    # print(currencies)
    # markets = ndax.fetch_markets()
    # print(markets)
    # ticker = ndax.fetch_ticker('DOGE/CAD')
    # print(ticker)
    # balance = ndax.fetch_balance()
    # print(balance)
    # fees = ndax.fetch_fees()
    # print(fees)
    # deposits = ndax.fetch_deposits()
    # print(deposits)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    grid_bot('TEST')
