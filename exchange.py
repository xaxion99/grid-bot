import file_loader
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

    def fetch_all_my_trades(self):
        my_trades = self.ndax.fetch_my_trades()
        file_loader.FileLoader().save_data(my_trades, 'data/accounts/my_trades.json')
        return my_trades

    def fetch_my_trades(self, file_path, symbol=None, since=None, limit=None):
        trades = self.ndax.fetch_my_trades(symbol=symbol, since=since, limit=limit)
        file_loader.FileLoader().save_data(trades, file_path)
        # Add code to interpret data recieved and return some desired values
        # Buys/Sells, Gross Buys/Gross Sells, Fees Cash/Fees Coin
        # Potentially add in Net Buys/Net Sells, Buy Fees/Sell Fees, Average Buy Cost/Average Sell Cost,
        #                    Average Buy Price/Average Sell Price
        orders = []
        for t in trades:
            orders.append({
                "amount": t['amount'],
                "cost": t['cost'],
                "datetime": t['datetime'],
                "fee": t['fee']['cost'],
                "fee_currency": t['fee']['currency'],
                "price": t['price'],
                "side": t['side'],
                "symbol": t['symbol'],
                "timestamp": t['timestamp'],
                "type": t['type']
            })

        # Interpret the data
        buy_count = 0
        sell_count = 0
        fee_coin = 0
        fee_cash = 0
        buy_amount = 0
        sell_amount = 0
        net_buy_amount = 0
        net_sell_amount = 0
        nf_buy = 0
        nf_sell = 0
        for o in orders:
            if o['side'] == 'buy':
                buy_count += 1
                fee_coin += float(o['fee'])
                buy_amount += ((float(o['amount']) - float(o['fee'])) * float(o['price']))
                net_buy_amount += (float(o['amount']) * float(o['price']))
                nf_buy += float(o['price'])
            if o['side'] == 'sell':
                sell_count += 1
                fee_cash += float(o['fee'])
                sell_amount += ((float(o['amount']) * float(o['price'])) - float(o['fee']))
                net_sell_amount += (float(o['amount']) * float(o['price']))
                nf_sell += float(o['price'])
        buy_amount = round(buy_amount, 8)
        sell_amount = round(sell_amount, 8)
        net_buy_amount = round(net_buy_amount, 8)
        net_sell_amount = round(net_sell_amount, 8)
        buy_fee = round(net_buy_amount - buy_amount, 8)
        sell_fee = round(net_sell_amount - sell_amount, 8)
        buy_avg = round(buy_amount / buy_count, 8)
        sell_avg = round(sell_amount / sell_count, 8)
        bp_avg = round(nf_buy / buy_count, 8)
        sp_avg = round(nf_sell / sell_count, 8)
        fee_coin = round(fee_coin, 8)
        fee_cash = round(fee_cash, 8)
        difference = round(sell_amount - buy_amount, 8)

        # Print out data
        with open('data/accounts/trading_summary.txt', 'a') as f:
            print('###################################################################################################',
                  file=f)
            if since and limit is not None:
                print('Summary from ' + str(since) + ' for ' + str(limit) + ' Data Points', file=f)
            elif since is not None:
                print('Summary from ' + str(since), file=f)
            elif limit is not None:
                print('Summary for last ' + str(limit) + ' Data Points', file=f)
            else:
                print('Summary of Trades', file=f)
            print('Buys: ' + str(buy_count) + ', Average Buy: ' + str(buy_avg), ', Average Price: ' + str(bp_avg),
                  file=f)
            print('Net: ' + str(net_buy_amount) + ', Gross: ' + str(buy_amount) + ', Fees: ' + str(buy_fee), file=f)
            print('Sells: ' + str(sell_count) + ', Average Sell: ' + str(sell_avg), ', Average Price: ' + str(sp_avg),
                  file=f)
            print('Net: ' + str(net_sell_amount) + ', Gross: ' + str(sell_amount) + ', Fees: ' + str(sell_fee), file=f)
            print('Actual Fees Cash: ' + str(fee_cash) + ', Actual Fees Coin: ' + str(fee_coin), file=f)
            if difference >= 0:
                print('Profit: ' + str(difference), file=f)
            else:
                print('Loss: ' + str(difference), file=f)
            print('###################################################################################################',
                  file=f)

        return trades

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
    def create_order(self, symbol, type, side, amount, price=None, stopprice=None):
        # self.ndax.create_order(symbol='DOGE/CAD', type='limit', side='buy', amount=100, price=0.08)
        # self.ndax.create_order(symbol='BTC/CAD', type='market', side='sell', amount=0.001, price=10)
        order = self.ndax.create_order(symbol, type, side, amount, price, stopprice)
        print(order)
        print('Order placed.')
        return order

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
        d = self.fl.load_plot_data(file_path)
        return d

    ####################################################################################################################
    # Other Functions
    def fetch_trades(self, pair):
        trades = self.ndax.fetch_trades(pair)
        print(trades)
        return trades
