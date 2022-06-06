import settings
import time
from datetime import datetime
from file_loader import FileLoader


class Strategy:
    def __init__(self, gt, exchange):
        self.grid = gt
        self.data = self.grid.get_data()
        self.num_of_intervals = self.grid.get_num_of_intervals()
        self.coins_per_interval = self.grid.get_coins_per_interval()
        self.amount_per_intervals = self.grid.get_amount_per_intervals()
        self.states = self.grid.get_states()
        self.state = self.grid.get_state()
        self.last_state = self.grid.get_last_state()
        self.min_val = self.grid.get_min_val()
        self.mid_val = self.grid.get_mid_val()
        self.max_val = self.grid.get_max_val()
        self.fee_rate = self.grid.get_fee_rate()
        self.tolerance = self.grid.get_tolerance()
        self.fl = FileLoader()
        self.ndax = exchange

    ####################################################################################################################
    # Paper Strategies
    def range_simulator(self, fiat=100, crypto=1000):
        with open('data/dummy_data/live_log.txt', 'w') as f:
            print('', file=f)
        count = 0
        # Fees
        fee_coin = 0
        fee_cash = 0
        # Transactions
        buys = 0
        sells = 0
        holds = 0
        # Trading Pairs
        cash = fiat  # Initial fiat for paper trade
        coins = crypto  # Initial crypto for paper trade
        init_cash = cash
        init_coins = coins
        # Current Price
        current_price = 0
        for val in self.data.keys():
            current_price = self.data[val]
            res = self.range_grid(id=count, price=self.data[val], cash=cash, coins=coins, fee_cash=fee_cash,
                                  fee_coin=fee_coin)
            count += 1
            cash = res[0]['cash']
            coins = res[0]['coins']

            if res[0]['fee_cash'] != 'None':
                fee_cash = res[0]['fee_cash']

            if res[0]['fee_coin'] != 'None':
                fee_coin = res[0]['fee_coin']

            if res[0]['type'] == 'buy':
                buys += 1
            elif res[0]['type'] == 'sell':
                sells += 1
            elif res[0]['type'] == 'hold':
                holds += 1
            else:
                break
        with open('data/dummy_data/simulation_results.txt', 'a') as f:
            print('##############################################################################################',
                  file=f)
            print('Range Paper Simulation Results', file=f)
            print('Intervals: ' + str(self.num_of_intervals) + ', # of Coins / Interval: ' +
                  str(self.coins_per_interval), file=f)
            print('Min: ' + str(self.min_val) + ', Mid: ' + str(self.mid_val) + ', Max: ' + str(self.max_val), file=f)
            print('Initial Coins: ' + str(init_coins) + ', Final Coins: ' + str(round(coins, self.tolerance)) +
                  ', Initial Cash: ' + str(init_cash) + ', Final Cash: ' + str(round(cash, self.tolerance)), file=f)
            print('Fees Crypto: ' + str(round(fee_coin, self.tolerance)), ', Fees Cash: ' +
                  str(round(fee_cash, self.tolerance)), file=f)
            print('Current Price: ' + str(round(current_price, self.tolerance)), file=f)
            initial_value = round((init_coins * current_price) + init_cash, self.tolerance)
            final_value = round((coins * current_price) + cash, self.tolerance)
            profits = round(final_value - initial_value, self.tolerance)
            perc_inc = round((profits / initial_value) * 100, self.tolerance)
            print('Initial Value: ' + str(initial_value) + ' Final Value: ' + str(final_value) + ', Profits: ' +
                  str(profits) + ', Increase: ' + str(perc_inc) + '%', file=f)
            print('Buys: ' + str(buys) + ', Sells: ' + str(sells) + ', Holds: ' + str(holds), file=f)
            print('##############################################################################################',
                  file=f)

    def trend_simulator(self, fiat=100, crypto=1000):
        with open('data/dummy_data/live_log.txt', 'w') as f:
            print('', file=f)
        count = 0
        # Fees
        fee_coin = 0
        fee_cash = 0
        # Transactions
        buys = 0
        sells = 0
        holds = 0
        # Trading Pairs
        cash = fiat  # Initial fiat for paper trade
        coins = crypto  # Initial crypto for paper trade
        init_cash = cash
        init_coins = coins
        # Current Price
        current_price = 0
        for val in self.data.keys():
            current_price = self.data[val]
            res = self.trend_grid(id=count, price=self.data[val], cash=cash, coins=coins, fee_cash=fee_cash,
                                  fee_coin=fee_coin)
            count += 1
            cash = res[0]['cash']
            coins = res[0]['coins']

            if res[0]['fee_cash'] != 'None':
                fee_cash = res[0]['fee_cash']

            if res[0]['fee_coin'] != 'None':
                fee_coin = res[0]['fee_coin']

            if res[0]['type'] == 'buy':
                buys += 1
            elif res[0]['type'] == 'sell':
                sells += 1
            elif res[0]['type'] == 'hold':
                holds += 1
            else:
                break
        with open('data/dummy_data/simulation_results.txt', 'a') as f:
            print('##############################################################################################',
                  file=f)
            print('Trend Paper Simulation Results', file=f)
            print('Intervals: ' + str(self.num_of_intervals) + ', # of Coins / Interval: ' +
                  str(self.coins_per_interval), file=f)
            print('Min: ' + str(self.min_val) + ', Mid: ' + str(self.mid_val) + ', Max: ' + str(self.max_val), file=f)
            print('Initial Coins: ' + str(init_coins) + ', Final Coins: ' + str(round(coins, self.tolerance)) +
                  ', Initial Cash: ' + str(init_cash) + ', Final Cash: ' + str(round(cash, self.tolerance)), file=f)
            print('Fees Crypto: ' + str(round(fee_coin, self.tolerance)), ', Fees Cash: ' +
                  str(round(fee_cash, self.tolerance)), file=f)
            print('Current Price: ' + str(round(current_price, self.tolerance)), file=f)
            initial_value = round((init_coins * current_price) + init_cash, self.tolerance)
            final_value = round((coins * current_price) + cash, self.tolerance)
            profits = round(final_value - initial_value, self.tolerance)
            perc_inc = round((profits / initial_value) * 100, self.tolerance)
            print('Initial Value: ' + str(initial_value) + ' Final Value: ' + str(final_value) + ', Profits: ' +
                  str(profits) + ', Increase: ' + str(perc_inc) + '%', file=f)
            print('Buys: ' + str(buys) + ', Sells: ' + str(sells) + ', Holds: ' + str(holds), file=f)
            print('##############################################################################################',
                  file=f)

    ####################################################################################################################
    # Live Strategies
    def live_trade(self, count,  c, tp, price='average', market='Ranging'):
        # Initialize variables
        fee_cash = 0
        fee_coin = 0
        buys = 0
        holds = 0
        sells = 0

        # Get ticker data
        current_ticker = self.ndax.fetch_ticker(tp)
        p = current_ticker[price]
        px = (current_ticker['ask'] + current_ticker['bid']) / 2
        p1 = current_ticker['bid']
        p2 = current_ticker['ask']
        p3 = current_ticker['vwap']
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string + ': { bid: ' + str(p1) + ', average_calc: ' + str(px) + ', ask: ' + str(p2) + ', vwap: ' +
              str(p3) + ' }')  # ', average: ' + str(p) +

        # Get balance on NDAX account
        balance = self.ndax.fetch_balance()
        cash = balance['CAD']['free']
        coins = balance[c]['free']

        # Get and plot updated data
        if count > 1000:
            ohlcv = self.ndax.fetch_ohlcv('data/live/live_ohlcv_data.json', tp, '1m', since=None, limit=1000)
        else:
            ohlcv = self.ndax.fetch_ohlcv('data/live/live_ohlcv_data.json', tp, '1m', since=None, limit=count)
        settings.ohlcv_data = ohlcv
        # settings.ticker_data.append([current_ticker['timestamp'], current_ticker['open'], current_ticker['high'],
        #                              current_ticker['low'], current_ticker['close'],
        #                              float(current_ticker['info']['Volume'])])

        # Check grid
        if market == 'Ranging':
            res = self.range_grid(id=count, price=px, cash=cash, coins=coins, fee_cash=fee_cash,
                                  fee_coin=fee_coin)
        elif market == 'Trending':
            res = self.trend_grid(id=count, price=px, cash=cash, coins=coins, fee_cash=fee_cash,
                                  fee_coin=fee_coin)

        # Set return data
        cash = res[0]['cash']
        coins = res[0]['coins']
        if res[0]['fee_cash'] != 'None':
            fee_cash = res[0]['fee_cash']
        if res[0]['fee_coin'] != 'None':
            fee_coin = res[0]['fee_coin']
        if res[0]['type'] == 'buy':
            buys += 1
            self.ndax.create_order(symbol=tp, type='limit', side='buy', amount=self.grid.get_coins_per_interval(), price=px)  # , price=p3
        elif res[0]['type'] == 'sell':
            sells += 1
            self.ndax.create_order(symbol=tp, type='limit', side='sell', amount=self.grid.get_coins_per_interval(), price=px)  # , price=p3
        elif res[0]['type'] == 'hold':
            holds += 1
        elif res[0]['type'] == 'break':
            return res[0]['current_state']  # return 'break' if the grid received a break command
        settings.trading_stats.append({
            'id': count,
            'cash': cash,
            'coins': coins,
            'fee_cash': fee_cash,
            'fee_coin': fee_coin,
            'buys': buys,
            'sells': sells,
            'holds': holds,
            'bid': p1,
            'ask': p2,
            'vwap': p3,
            'calc_mid': px
        })
        self.fl.save_data(settings.trading_stats, 'data/live/trading_stats.json')
        return current_ticker

    ####################################################################################################################
    # Generalized range grid function
    def range_grid(self, id, price, cash, coins, fee_cash, fee_coin):
        amount = self.coins_per_interval * float(price)
        result = []
        for v in self.states.values():
            if (float(price) >= v) and (float(price) < (v + self.amount_per_intervals)):
                self.last_state = self.states[self.state]
                self.state = self.grid.get_key(v)
                break
        c_state = self.states[self.state]
        if float(price) < self.states[0]:
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'break',
                'coins': coins,
                'cash': cash,
                'fee_cash': 'None',
                'fee_coin': 'None',
                'current_state': 'Low Safe',
                'next_state': 'None'
            })
        elif float(price) > self.states[self.num_of_intervals]:
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'break',
                'coins': coins,
                'cash': cash,
                'fee_cash': 'None',
                'fee_coin': 'None',
                'current_state': 'High Safe',
                'next_state': 'None'
            })
        elif float(price) >= self.last_state and coins >= self.coins_per_interval \
                and c_state != self.last_state:
            fee_amount = round(self.fee_rate * amount, self.tolerance)
            fee_cash += fee_amount
            coins -= self.coins_per_interval
            cash += round(amount - fee_amount, self.tolerance)
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'sell',
                'coins': coins,
                'cash': cash,
                'fee_cash': fee_cash,
                'fee_coin': 'None',
                'current_state': self.last_state,
                'next_state': self.states[self.state]
            })
        elif float(price) < self.last_state and cash >= amount and c_state != self.last_state:
            fee_amount = round(self.fee_rate * self.coins_per_interval, self.tolerance)
            fee_coin += fee_amount
            cash -= round(amount, self.tolerance)
            coins += round(self.coins_per_interval - fee_amount, self.tolerance)
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'buy',
                'coins': coins,
                'cash': cash,
                'fee_cash': 'None',
                'fee_coin': fee_coin,
                'current_state': self.last_state,
                'next_state': self.states[self.state]
            })
        else:
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'hold',
                'coins': coins,
                'cash': cash,
                'fee_cash': 'None',
                'fee_coin': 'None',
                'current_state': self.last_state,
                'next_state': self.states[self.state]
            })
        with open('data/live/live_log.txt', 'a') as f:
            print(result, file=f)
        return result

    ####################################################################################################################
    # Generalized trend grid function
    def trend_grid(self, id, price, cash, coins, fee_cash, fee_coin):
        amount = self.coins_per_interval * float(price)
        result = []
        for v in self.states.values():
            if (float(price) >= v) and (float(price) < (v + self.amount_per_intervals)):
                self.last_state = self.states[self.state]
                self.state = self.grid.get_key(v)
                break
        c_state = self.states[self.state]
        if float(price) < self.states[0]:
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'break',
                'coins': coins,
                'cash': cash,
                'fee_cash': 'None',
                'fee_coin': 'None',
                'current_state': 'Low Safe',
                'next_state': 'None'
            })
        elif float(price) > self.states[self.num_of_intervals]:
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'break',
                'coins': coins,
                'cash': cash,
                'fee_cash': 'None',
                'fee_coin': 'None',
                'current_state': 'High Safe',
                'next_state': 'None'
            })
        elif float(price) >= self.last_state and cash >= amount and c_state != self.last_state:
            fee_amount = round(self.fee_rate * self.coins_per_interval, self.tolerance)
            fee_coin += fee_amount
            cash -= round(amount, self.tolerance)
            coins += round(self.coins_per_interval - fee_amount, self.tolerance)
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'buy',
                'coins': coins,
                'cash': cash,
                'fee_cash': 'None',
                'fee_coin': fee_coin,
                'current_state': self.last_state,
                'next_state': self.states[self.state]
            })
        elif float(price) < self.last_state and coins >= self.coins_per_interval and c_state != self.last_state:
            fee_amount = round(self.fee_rate * amount, self.tolerance)
            fee_cash += fee_amount
            coins -= self.coins_per_interval
            cash += round(amount - fee_amount, self.tolerance)
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'sell',
                'coins': coins,
                'cash': cash,
                'fee_cash': fee_cash,
                'fee_coin': 'None',
                'current_state': self.last_state,
                'next_state': self.states[self.state]
            })
        else:
            result.append({
                'id': id,
                'amount': float(price),
                'type': 'hold',
                'coins': coins,
                'cash': cash,
                'fee_cash': 'None',
                'fee_coin': 'None',
                'current_state': self.last_state,
                'next_state': self.states[self.state]
            })
        with open('data/live/live_log.txt', 'a') as f:
            print(result, file=f)
        return result
