import json
import statistics
from scipy.stats import skew

from strategy import Strategy


class Test:
    def __init__(self):
        pass

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
