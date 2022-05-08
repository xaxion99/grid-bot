import csv
import json


class FileLoader:

    def __init__(self):
        print('File loader initialized.')

    # Load dummy data from a CSV
    def load_dummy_data(self, file_path):
        d = []
        csv_file = open(file_path)
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            for col in row:
                d.append(col)
                line_count += 1
        print(f'Processed {line_count} data points.')
        c_arr = list(range(1, line_count + 1))
        data = dict(zip(c_arr, d))
        # d.reverse()
        # data = dict(zip(c_arr, d))
        return data

    # Load data from a JSON file
    def load_data(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            arr1 = []
            data_points = 0
            for d in data:
                data_points += 1
                arr1.append(d)
            print(f'Loaded {data_points} data points.')
            c_arr = list(range(1, data_points + 1))
            arr = []
            for a in arr1:
                arr.append(a[1])
            a = dict(zip(c_arr, arr))
            return a

    # Save data to a JSON file
    def save_data(self, arr, file_path):
        with open(file_path, 'w') as outfile:
            json.dump(arr, outfile)
