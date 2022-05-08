from file_loader import FileLoader


class Grid:
    data = {}
    states = {}
    cash = 100
    coins = 1000

    def __init__(self, i=0, mn_v=0, mx_v=0, cpi=0, dp=3):
        self.num_of_intervals = i
        self.tolerance = dp
        self.min_val = mn_v
        self.max_val = mx_v
        self.mid_val = round((mx_v + mn_v) / 2, dp)
        self.difference = mx_v - mn_v
        if i != 0:
            self.amount_per_intervals = round((mx_v - mn_v) / i, dp)
        else:
            self.amount_per_intervals = 0
        self.coins_per_interval = cpi
        self.state = i / 2
        self.create_states()
        self.last_state = self.states[self.state]
        self.fl = FileLoader()

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
        print(self.states)

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
                fees += round(0.002 * amount, self.tolerance)
                self.cash += round(amount - (0.002 * amount), self.tolerance)
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
                fees += round(0.002 * amount, self.tolerance)
                self.cash -= round(amount + (0.002 * amount), self.tolerance)
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
        print('Coins: ' + str(self.coins) + ', Cash: ' + str(round(self.cash, self.tolerance)) + ', Fee Paid: ' +
              str(round(fees, self.tolerance)))
        print('Buys: ' + str(buys) + ', Sells: ' + str(sells) + ', Holds: ' + str(holds))
        self.fl.save_data(array, 'grid_data.json')

    # Getters
    def get_data(self):
        return self.data

    # Setters
    def set_data(self, data):
        self.data = data
