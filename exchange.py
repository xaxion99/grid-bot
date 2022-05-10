from file_loader import FileLoader


class Exchange:

    def __init__(self, exchange):
        self.ndax = exchange
        self.fl = FileLoader()

    def fetch_accounts(self):
        accounts = self.ndax.fetch_accounts()
        print(accounts)
        return accounts

    def fetch_balance(self):
        balance = self.ndax.fetch_balance()
        print(balance)
        return balance

    def fetch_currencies(self):
        currencies = self.ndax.fetch_currencies()
        print(currencies)
        return currencies

    def fetch_deposit_address(self):
        deposit_address = self.ndax.fetch_deposit_address()
        print(deposit_address)
        return deposit_address

    def fetch_deposits(self):
        deposits = self.ndax.fetch_deposits()
        print(deposits)
        return deposits

    def fetch_ledger(self):
        ledger = self.ndax.fetch_ledger()
        print(ledger)
        return ledger

    def fetch_markets(self):
        markets = self.ndax.fetch_markets()
        print(markets)
        return markets

    def fetch_my_trades(self):
        my_trades = self.ndax.fetch_my_trades()
        print(my_trades)
        return my_trades

    def fetch_ohlcv(self, file_path='data/ndax_data_08_May_22.json', pair='DOGE/CAD', tf='1m', since=1651966200):
        # OHLC(V) Candle Retriever
        ohlcv = self.ndax.fetch_ohlcv(pair, timeframe=tf, since=since)  # since= uses UNIX time
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

    def fetch_order(self):
        order = self.ndax.fetch_order()
        print(order)
        return order

    def fetch_orders(self):
        orders = self.ndax.fetch_orders()
        print(orders)
        return orders

    def fetch_order_book(self, pair):
        order_book = self.ndax.fetch_order_book(pair)
        print(order_book)
        return order_book

    def fetch_order_trades(self):
        order_trades = self.ndax.fetch_order_trades()
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
