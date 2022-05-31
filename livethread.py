import threading
import time
from file_loader import FileLoader


class LiveThread(threading.Thread):
    def __init__(self, s):
        self.s = s
        self.fl = FileLoader()
        super(LiveThread, self).__init__()
        self.__stop = threading.Event()

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.isSet()

    def run(self):
        # Setup loop variables
        self.arr = []
        count = 0
        while not self.stopped():
            # Put your script execution here
            count += 1
            res = self.s.live_trade(count, 'DOGE', 'DOGE/CAD', 'average')
            if res == 'Low Safe' or res == 'High Safe':
                time.sleep(3)
                self.stop()
                print('Successfully broke loop!')
            else:
                self.arr.append(res)
                self.fl.save_data(self.arr, 'data/live/ticker.json')
                time.sleep(59)
