import threading
import time
from datetime import datetime

import matplotlib.animation as animation
import matplotlib.pyplot as plt


class LiveThread(threading.Thread):
    def __init__(self, s, fig):
        self.s = s
        self.fig = fig
        super(LiveThread, self).__init__()
        self.__stop = threading.Event()

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.isSet()

    def run(self):
        # Setup Matplotlib
        self.ax1 = self.fig.add_subplot(1, 1, 1)

        # Setup loop variables
        live = True
        self.arr = []
        count = 0
        fee_cash = 0
        fee_coin = 0
        while not self.stopped():
            # Put your script execution here
            count += 1
            self.arr.append(self.s.live_trade('DOGE', 'DOGE/CAD', 'average'))
            ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
            time.sleep(59)

    def animate(self):
        data = self.arr
        bidarr = []
        avgarr = []
        askarr = []
        yarr = []
        for d in data:
            bid = d['bid']
            avg = d['average']
            ask = d['ask']
            # y = datetime.utcfromtimestamp(d['timestamp']).strftime('%D-%M-%Y %H:%M:%S')
            y = d['timestamp']
            bidarr.append(int(bid))
            avgarr.append(int(avg))
            avgarr.append(int(ask))
            yarr.append(int(y))

        self.ax1.clear()
        self.ax1.plot(bidarr, yarr)
        self.ax1.plot(avgarr, yarr)
        self.ax1.plot(askarr, yarr)
