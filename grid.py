from file_loader import FileLoader


class GridTrade:
    data = {}  # Dictionary to hold any preloaded data
    states = {}  # Dictionary to store the grid states
    cash = 100  # Initial fiat for paper trade
    coins = 1000  # Initial crypto for paper trade
    fee_rate = 0.002  # Percentage fee rate, NDAX's is 0.2%

    def __init__(self, i, mn_v, mx_v, cpi, dp):
        self.num_of_intervals = i  # Needs to be even
        self.tolerance = dp  # Number of decimal places to round to
        self.min_val = mn_v  # Minimum value of grid
        self.max_val = mx_v  # Maximum value of grid
        self.mid_val = round((mx_v + mn_v) / 2, dp)  # Mid value of grid
        self.difference = mx_v - mn_v  # Difference between max and min
        if i != 0:
            self.amount_per_intervals = round((mx_v - mn_v) / i, dp)  # Cash range of interval
        else:
            self.amount_per_intervals = 0
        self.coins_per_interval = cpi  # How many of crypto to buy/sell on grid state change
        self.state = i / 2  # State of the bot, initialize to middle interval
        self.create_states()  # Generate a list of all the states and there bounds
        self.last_state = self.states[self.state]  # The previous state, used to check if state has changed
        self.fl = FileLoader()  # Create a FileLoader object

    # Create the grid states which are bounded by stored values
    def create_states(self):
        arr1 = list(range(0, self.num_of_intervals + 1))
        arr2 = []
        i = 0
        while i < len(arr1):
            val = round(self.min_val + (i * self.amount_per_intervals), self.tolerance)
            arr2.append(val)
            i += 1
        self.states = dict(zip(arr1, arr2))
        print(f'State Boundaries: {self.states}')

    # Get the Dictionary key from the value
    def get_key(self, val):
        for key, value in self.states.items():
            if val == value:
                return key
        return self.state

    def simulator(self):
        array = []
        fees = 0
        buys = 0
        sells = 0
        holds = 0
        for val in self.data.keys():
            amount = self.coins_per_interval * float(self.data[val])
            for v in self.states.values():
                if (float(self.data[val]) >= v) and (float(self.data[val]) < (v + self.amount_per_intervals)):
                    self.last_state = self.states[self.state]
                    self.state = self.get_key(v)
                    break
            c_state = self.states[self.state]
            if float(self.data[val]) < self.states[0]:
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'break',
                    'coins': self.coins,
                    'cash': self.cash,
                    'current_state': 'Low Safe',
                    'next_state': 'None'
                })
                break
            elif float(self.data[val]) > self.states[self.num_of_intervals]:
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'break',
                    'coins': self.coins,
                    'cash': self.cash,
                    'current_state': 'High Safe',
                    'next_state': 'None'
                })
                break
            elif float(self.data[val]) >= self.last_state and self.coins >= self.coins_per_interval \
                    and c_state != self.last_state:
                self.coins -= self.coins_per_interval
                fees += round(self.fee_rate * amount, self.tolerance)
                self.cash += round(amount - (self.fee_rate * amount), self.tolerance)
                sells += 1
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'sell',
                    'coins': self.coins,
                    'cash': self.cash,
                    'current_state': self.last_state,
                    'next_state': self.states[self.state]
                })
            elif float(self.data[val]) < self.last_state and self.cash >= amount and c_state != self.last_state:
                self.coins += self.coins_per_interval
                fees += round(self.fee_rate * amount, self.tolerance)
                self.cash -= round(amount + (self.fee_rate * amount), self.tolerance)
                buys += 1
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'buy',
                    'coins': self.coins,
                    'cash': self.cash,
                    'current_state': self.last_state,
                    'next_state': self.states[self.state]
                })
            else:
                holds += 1
                array.append({
                    'id': val,
                    'amount': float(self.data[val]),
                    'type': 'hold',
                    'coins': self.coins,
                    'cash': self.cash,
                    'current_state': self.last_state,
                    'next_state': self.states[self.state]
                })
        print('Min: ' + str(self.min_val) + ', Mid: ' + str(self.mid_val) + ', Max: ' + str(self.max_val))
        print('Coins: ' + str(self.coins) + ', Cash: ' + str(round(self.cash, self.tolerance)))
        initial_value = round((1000 * self.mid_val) + 100, self.tolerance)
        final_value = round((self.coins * self.mid_val) + self.cash, self.tolerance)
        profits = round(final_value - initial_value, self.tolerance)
        perc_inc = round((profits / initial_value) * 100, self.tolerance)
        print('Initial Value: ' + str(initial_value) + ', Final Value: ' + str(final_value) + ', Profits: ' +
              str(profits) + ', % Increase: ' + str(perc_inc) + '% , Fee Paid: ' + str(round(fees, self.tolerance)))
        print('Buys: ' + str(buys) + ', Sells: ' + str(sells) + ', Holds: ' + str(holds))
        self.fl.save_data(array, 'data/grid_data.json')

    # Getters
    def get_data(self):
        return self.data

    # Setters
    def set_data(self, data):
        self.data = data
