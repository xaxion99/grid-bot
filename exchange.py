import file_loader
from file_loader import FileLoader


class Exchange:

    def __init__(self, exchange):
        self.ndax = exchange
        self.fl = FileLoader()

    # Fetch Functions
    def fetch_accounts(self):
        accounts = self.ndax.fetch_accounts()
        print('Account: ')
        print(accounts)
        return accounts

    def fetch_balance(self):
        balance = self.ndax.fetch_balance()
        print('Free: ')
        print(balance['free'])
        print('Used: ')
        print(balance['used'])
        print('Total: ')
        print(balance['total'])
        file_loader.FileLoader().save_data(balance, 'data/balance.json')
        return balance

    def fetch_currency(self, c):
        currencies = self.ndax.fetch_currencies()
        # print(currencies)
        print(c)
        print(currencies[c])
        return currencies

    def fetch_currencies(self):
        currencies = self.ndax.fetch_currencies()
        # print(currencies)
        print(currencies.keys())
        file_loader.FileLoader().save_data(currencies, 'data/currencies.json')
        return currencies

    def fetch_deposit_address(self):
        deposit_address = self.ndax.fetch_deposit_address()
        print(deposit_address)
        return deposit_address

    def fetch_deposits(self):
        deposits = self.ndax.fetch_deposits()
        file_loader.FileLoader().save_data(deposits, 'data/deposits.json')
        return deposits

    def fetch_ledger(self):
        ledger = self.ndax.fetch_ledger()
        file_loader.FileLoader().save_data(ledger, 'data/ledger.json')
        return ledger

    def fetch_markets(self):
        markets = self.ndax.fetch_markets()
        file_loader.FileLoader().save_data(markets, 'data/markets.json')
        return markets

    def fetch_my_trades(self):
        my_trades = self.ndax.fetch_my_trades()
        file_loader.FileLoader().save_data(my_trades, 'data/my_trades.json')
        return my_trades

    def fetch_ohlcv(self, file_path, pair='DOGE/CAD', tf='1m', since=None, limit=None):
        # OHLC(V) Candle Retriever
        ohlcv = self.ndax.fetch_ohlcv(pair, timeframe=tf, since=since, limit=limit)  # since= uses UNIX time
        self.fl.save_data(ohlcv, file_path)
        # Check basic stats of the retrieved data
        d = self.fl.load_data(file_path)
        print(f'Min: {min(d.values())}')
        print(f'Mid: {(min(d.values()) + max(d.values())) / 2}')
        print(f'Max: {max(d.values())}')
        return ohlcv

    def fetch_open_orders(self):
        open_orders = self.ndax.fetch_open_orders()
        print(open_orders)
        return open_orders

    def fetch_order(self, id):
        order = self.ndax.fetch_order(id)
        print(order)
        return order

    def fetch_orders(self):
        orders = self.ndax.fetch_orders()
        file_loader.FileLoader().save_data(orders, 'data/orders.json')
        return orders

    def fetch_order_book(self, pair):
        order_book = self.ndax.fetch_order_book(pair)
        print(order_book)
        return order_book

    def fetch_order_trades(self, id):
        order_trades = self.ndax.fetch_order_trades(id)
        print(order_trades)
        return order_trades

    def fetch_ticker(self, pair):
        ticker = self.ndax.fetch_ticker(pair)
        print(ticker)
        return ticker

    def fetch_trades(self, pair):
        trades = self.ndax.fetch_trades(pair)
        print(trades)
        return trades

    def fetch_withdrawals(self):
        withdrawals = self.ndax.fetch_withdrawals()
        print(withdrawals)
        return withdrawals

    # Orders Functions
    def create_order(self, symbol, type, side, amount, price):
        order = self.ndax.create_order(symbol, type, side, amount, price)
        print(order)
        print('Order placed.')

    def edit_order(self, id, symbol, type, side, amount):
        order = self.ndax.edit_order(id, symbol, type, side, amount, price=None, params={})
        print('Order edited.')

    def cancel_order(self, id):
        res = self.ndax.cancel_order(id, symbol=None, params={})
        print('All orders cancelled.')

    def cancel_all_orders(self):
        res = self.ndax.cancel_all_orders(symbol=None, params={})
        print('All orders cancelled.')
