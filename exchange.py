import file_loader
import statistics
from file_loader import FileLoader


class Exchange:
    def __init__(self, exchange):
        self.ndax = exchange
        self.fl = FileLoader()

    ####################################################################################################################
    # Account Functions
    def fetch_accounts(self):
        accounts = self.ndax.fetch_accounts()
        file_loader.FileLoader().save_data(accounts, 'data/accounts/accounts.json')
        return accounts

    def fetch_balance(self):
        balance = self.ndax.fetch_balance()
        file_loader.FileLoader().save_data(balance, 'data/accounts/balance.json')
        return balance

    # Untested
    def fetch_deposit_address(self):
        deposit_address = self.ndax.fetch_deposit_address()
        print(deposit_address)
        return deposit_address

    def fetch_deposits(self):
        deposits = self.ndax.fetch_deposits()
        file_loader.FileLoader().save_data(deposits, 'data/accounts/deposits.json')
        return deposits

    def fetch_ledger(self):
        ledger = self.ndax.fetch_ledger()
        file_loader.FileLoader().save_data(ledger, 'data/accounts/ledger.json')
        return ledger

    def fetch_my_trades(self):
        my_trades = self.ndax.fetch_my_trades()
        file_loader.FileLoader().save_data(my_trades, 'data/accounts/my_trades.json')
        return my_trades

    # Untested
    def fetch_withdrawals(self):
        withdrawals = self.ndax.fetch_withdrawals()
        print(withdrawals)
        return withdrawals

    ####################################################################################################################
    # Order Functions
    def fetch_open_orders(self):
        open_orders = self.ndax.fetch_open_orders()
        file_loader.FileLoader().save_data(open_orders, 'data/orders/open_orders.json')
        return open_orders

    # Untested
    def fetch_order(self, id):
        order = self.ndax.fetch_order(id)
        print(order)
        return order

    def fetch_orders(self):
        orders = self.ndax.fetch_orders()
        file_loader.FileLoader().save_data(orders, 'data/orders/orders.json')
        return orders

    # Untested
    def fetch_order_book(self, pair):
        order_book = self.ndax.fetch_order_book(pair)
        print(order_book)
        return order_book

    # Untested
    def fetch_order_trades(self, id):
        order_trades = self.ndax.fetch_order_trades(id)
        print(order_trades)
        return order_trades

    # Create Order
    def create_order(self, symbol, type, side, amount, price):
        order = self.ndax.create_order(symbol, type, side, amount, price)
        print(order)
        print('Order placed.')

    # Edit/Update Order
    # Untested
    def edit_order(self, id, symbol, type, side, amount):
        order = self.ndax.edit_order(id, symbol, type, side, amount, price=None, params={})
        print('Order edited.')

    # Cancel/Delete Order(s)
    # Untested
    def cancel_order(self, id):
        res = self.ndax.cancel_order(id, symbol=None, params={})
        print('All orders cancelled.')

    def cancel_all_orders(self):
        res = self.ndax.cancel_all_orders(symbol=None, params={})
        print('All orders cancelled.')

    ####################################################################################################################
    # NDAX Functions
    def fetch_currency(self, c):
        currencies = self.ndax.fetch_currencies()
        file_loader.FileLoader().save_data(currencies[c], 'data/ndax/currency.json')
        return currencies

    def fetch_currencies(self):
        currencies = self.ndax.fetch_currencies()
        file_loader.FileLoader().save_data(currencies, 'data/ndax/currencies.json')
        return currencies

    def fetch_market(self, tp):
        markets = self.ndax.fetch_markets()
        for m in markets:
            if m['symbol'] == tp:
                file_loader.FileLoader().save_data(m, 'data/ndax/market.json')
                return m
        return []

    def fetch_markets(self):
        markets = self.ndax.fetch_markets()
        file_loader.FileLoader().save_data(markets, 'data/ndax/markets.json')
        return markets

    def fetch_ticker(self, pair):
        ticker = self.ndax.fetch_ticker(pair)
        file_loader.FileLoader().save_data(ticker, 'data/ndax/current_ticker.json')
        return ticker

    def fetch_trading_pairs(self):
        markets = self.ndax.fetch_markets()
        trading_pairs = []
        for m in markets:
            trading_pairs.append(m['symbol'])
        return trading_pairs

    ####################################################################################################################
    # OHLC(V) Functions
    def fetch_ohlcv(self, file_path, pair, tf, since=None, limit=None):
        #     [
        #         1501603632000,  # 0 DateTime
        #         2700.33,       # 1 High
        #         2687.01,       # 2 Low
        #         2687.01,       # 3 Open
        #         2687.01,       # 4 Close
        #         24.86100992,   # 5 Volume
        #         0,             # 6 Inside Bid Price
        #         2870.95,       # 7 Inside Ask Price
        #         1              # 8 InstrumentId
        #     ]
        # OHLC(V) Candle Retriever
        ohlcv = self.ndax.fetch_ohlcv(pair, timeframe=tf, since=since, limit=limit)  # since= uses UNIX time
        self.fl.save_data(ohlcv, file_path)
        # Check basic stats of the retrieved data
        d = self.fl.load_data(file_path)
        return d

    ####################################################################################################################
    # Other Functions
    def fetch_trades(self, pair):
        trades = self.ndax.fetch_trades(pair)
        print(trades)
        return trades
