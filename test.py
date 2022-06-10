import json
import statistics
from grid import GridTrade
from scipy.stats import skew
from strategy import Strategy


class Test:
    def __init__(self, xc):
        self.ndax = xc

    def test(self):
        g = GridTrade(10, 0.095, 0.105, 200, 8, self.ndax)
        s = Strategy(g, self.ndax)
        t = []
        t.append(s.trad_grid(-1, 0.106, 50, 1000))
        t.append(s.trad_grid(0, 0.1046, 50, 1000))
        t.append(s.trad_grid(1, 0.1, 50, 1000))
        t.append(s.trad_grid(2, 0.103, 50, 1000))
        t.append(s.trad_grid(3, 0.095, 50, 1000))
        t.append(s.trad_grid(4, 0.105, 50, 1000))
        t.append(s.trad_grid(5, 0.094, 50, 1000))
        for i in t:
            print(i)

    def load_ticker_data(self):
        with open('data/ticker_data.json', 'r') as f:
            data = json.load(f)
        array = []
        count = 0
        total = 0
        for d in data:
            count += 1
            total += d['last']
            array.append(d['last'])
        print(array)
        mean = statistics.mean(array)
        median = statistics.median(array)
        s = skew(array)
        print('Max: ' + str(max(array)) + ' Min: ' + str(min(array)))
        print('Mean: ' + str(mean) + ' Median: ' + str(median))
        print('Skew: ' + str(s) + ' # of Data Points: ' + str(count))
