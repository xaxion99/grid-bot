import time
from exchange import Exchange
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

    def range_simulator(self, fiat=100, crypto=1000):
        array = []
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
            amount = self.coins_per_interval * float(self.data[val])
            for v in self.states.values():
                if (float(self.data[val]) >= v) and (float(self.data[val]) < (v + self.amount_per_intervals)):
                    self.last_state = self.states[self.state]
                    self.state = self.grid.get_key(v)
                    break
            c_state = self.states[self.state]
            if float(self.data[val]) < self.states[0]:
                current_price = float(self.data[val])
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'break',
                    'coins': coins,
                    'cash': cash,
                    'fees': 'None',
                    'current_state': 'Low Safe',
                    'next_state': 'None'
                })
                break
            elif float(self.data[val]) > self.states[self.num_of_intervals]:
                current_price = float(self.data[val])
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'break',
                    'coins': coins,
                    'cash': cash,
                    'fees': 'None',
                    'current_state': 'High Safe',
                    'next_state': 'None'
                })
                break
            elif float(self.data[val]) >= self.last_state and coins >= self.coins_per_interval \
                    and c_state != self.last_state:
                current_price = float(self.data[val])
                fee_amount = round(self.fee_rate * amount, self.tolerance)
                fee_cash += fee_amount
                coins -= self.coins_per_interval
                cash += round(amount - fee_amount, self.tolerance)
                sells += 1
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'sell',
                    'coins': coins,
                    'cash': cash,
                    'fees': fee_amount,
                    'current_state': self.last_state,
                    'next_state': self.states[self.state]
                })
            elif float(self.data[val]) < self.last_state and cash >= amount and c_state != self.last_state:
                current_price = float(self.data[val])
                fee_amount = round(self.fee_rate * self.coins_per_interval, self.tolerance)
                fee_coin += fee_amount
                cash -= round(amount, self.tolerance)
                coins += round(self.coins_per_interval - fee_amount, self.tolerance)
                buys += 1
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'buy',
                    'coins': coins,
                    'cash': cash,
                    'fees': fee_amount,
                    'current_state': self.last_state,
                    'next_state': self.states[self.state]
                })
            else:
                current_price = float(self.data[val])
                holds += 1
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'hold',
                    'coins': coins,
                    'cash': cash,
                    'fees': 'None',
                    'current_state': self.last_state,
                    'next_state': self.states[self.state]
                })
        print('#######################################################################################################')
        print('Range Paper Simulation Results')
        print('Min: ' + str(self.min_val) + ', Mid: ' + str(self.mid_val) + ', Max: ' + str(self.max_val))
        print('Initial Coins: ' + str(init_coins) + ', Final Coins: ' + str(round(coins, self.tolerance)) +
              ', Initial Cash: ' + str(init_cash) + ', Final Cash: ' + str(round(cash, self.tolerance)))
        print('Fees Crypto: ' + str(round(fee_coin, self.tolerance)), ', Fees Cash: ' +
              str(round(fee_cash, self.tolerance)))
        print('Current Price: ' + str(round(current_price, self.tolerance)))
        initial_value = round((init_coins * current_price) + init_cash, self.tolerance)
        final_value = round((coins * current_price) + cash, self.tolerance)
        profits = round(final_value - initial_value, self.tolerance)
        perc_inc = round((profits / initial_value) * 100, self.tolerance)
        print('Initial Value: ' + str(initial_value) + ' Final Value: ' + str(final_value) + ', Profits: ' +
              str(profits) + ', Increase: ' + str(perc_inc) + '%')
        print('Buys: ' + str(buys) + ', Sells: ' + str(sells) + ', Holds: ' + str(holds))
        print('#######################################################################################################')
        self.fl.save_data(array, 'data/grid_data.json')

    def trend_simulator(self, fiat=100, crypto=1000):
        array = []
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
            amount = self.coins_per_interval * float(self.data[val])
            for v in self.states.values():
                if (float(self.data[val]) >= v) and (float(self.data[val]) < (v + self.amount_per_intervals)):
                    self.last_state = self.states[self.state]
                    self.state = self.grid.get_key(v)
                    break
            c_state = self.states[self.state]
            if float(self.data[val]) < self.states[0]:
                current_price = float(self.data[val])
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'break',
                    'coins': coins,
                    'cash': cash,
                    'fees': 'None',
                    'current_state': 'Low Safe',
                    'next_state': 'None'
                })
                break
            elif float(self.data[val]) > self.states[self.num_of_intervals]:
                current_price = float(self.data[val])
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'break',
                    'coins': coins,
                    'cash': cash,
                    'fees': 'None',
                    'current_state': 'High Safe',
                    'next_state': 'None'
                })
                break
            elif float(self.data[val]) >= self.last_state and coins >= self.coins_per_interval \
                    and c_state != self.last_state:
                current_price = float(self.data[val])
                fee_amount = round(self.fee_rate * self.coins_per_interval, self.tolerance)
                fee_coin += fee_amount
                cash -= round(amount, self.tolerance)
                coins += round(self.coins_per_interval - fee_amount, self.tolerance)
                buys += 1
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'buy',
                    'coins': coins,
                    'cash': cash,
                    'fees': fee_amount,
                    'current_state': self.last_state,
                    'next_state': self.states[self.state]
                })
            elif float(self.data[val]) < self.last_state and cash >= amount and c_state != self.last_state:
                current_price = float(self.data[val])
                fee_amount = round(self.fee_rate * amount, self.tolerance)
                fee_cash += fee_amount
                coins -= self.coins_per_interval
                cash += round(amount - fee_amount, self.tolerance)
                sells += 1
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'sell',
                    'coins': coins,
                    'cash': cash,
                    'fees': fee_amount,
                    'current_state': self.last_state,
                    'next_state': self.states[self.state]
                })
            else:
                current_price = float(self.data[val])
                holds += 1
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'hold',
                    'coins': coins,
                    'cash': cash,
                    'fees': 'None',
                    'current_state': self.last_state,
                    'next_state': self.states[self.state]
                })
        print('#######################################################################################################')
        print('Trend Paper Simulation Results')
        print('Min: ' + str(self.min_val) + ', Mid: ' + str(self.mid_val) + ', Max: ' + str(self.max_val))
        print('Initial Coins: ' + str(init_coins) + ', Final Coins: ' + str(round(coins, self.tolerance)) +
              ', Initial Cash: ' + str(init_cash) + ', Final Cash: ' + str(round(cash, self.tolerance)))
        print('Fees Crypto: ' + str(round(fee_coin, self.tolerance)), ', Fees Cash: ' +
              str(round(fee_cash, self.tolerance)))
        print('Current Price: ' + str(round(current_price, self.tolerance)))
        initial_value = round((init_coins * current_price) + init_cash, self.tolerance)
        final_value = round((coins * current_price) + cash, self.tolerance)
        profits = round(final_value - initial_value, self.tolerance)
        perc_inc = round((profits / initial_value) * 100, self.tolerance)
        print('Initial Value: ' + str(initial_value) + ' Final Value: ' + str(final_value) + ', Profits: ' +
              str(profits) + ', Increase: ' + str(perc_inc) + '%')
        print('Buys: ' + str(buys) + ', Sells: ' + str(sells) + ', Holds: ' + str(holds))
        print('#######################################################################################################')
        self.fl.save_data(array, 'data/grid_data.json')

    # Live Trade
    def live_trade(self):
        live = True
        arr = []
        count = 0
        while live:
            arr.append(self.ndax.fetch_ticker('DOGE/CAD'))
            time.sleep(60)
            if count == 59:
                live = False
            else:
                count += 1
        self.fl.save_data(arr, 'data/ticker_data.json')
