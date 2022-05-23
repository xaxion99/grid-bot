from file_loader import FileLoader


class GridTrade:
    data = {}  # Dictionary to hold any preloaded data
    states = {}  # Dictionary to store the grid states
    fee_rate = 0.002  # Percentage fee rate, NDAX's is 0.2%

    def __init__(self, i, mn_v, mx_v, cpi, dp, xc):
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
        self.ndax = xc

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

    # Getters
    def get_data(self):
        return self.data

    def get_states(self):
        return self.states

    def get_fee_rate(self):
        return self.fee_rate

    def get_num_of_intervals(self):
        return self.num_of_intervals

    def get_tolerance(self):
        return self.tolerance

    def get_min_val(self):
        return self.min_val

    def get_mid_val(self):
        return self.mid_val

    def get_max_val(self):
        return self.max_val

    def get_difference(self):
        return self.difference

    def get_amount_per_intervals(self):
        return self.amount_per_intervals

    def get_coins_per_interval(self):
        return self.coins_per_interval

    def get_state(self):
        return self.state

    def get_last_state(self):
        return self.last_state

    # Setters
    def set_data(self, data):
        self.data = data
