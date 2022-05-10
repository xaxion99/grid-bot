from exchange import Exchange
from file_loader import FileLoader
from grid import GridTrade
from tkinter import *


class GUI:

    def __init__(self, master, login):
        self.master = master
        self.ndax = Exchange(login)
        self.fl = FileLoader()

        # Setup the master window
        master.title("NDAX Grid Trading Bot")
        # master.wm_iconbitmap('Icons/logo_large.ico')  # Add logo to top bar
        # master.resizable(height = None, width = None)
        master.resizable(0, 0)  # Make window not resizable (resizing is broken atm)

        ################################################################################################################
        # Frames
        self.ndaxFrame = Frame(master, borderwidth=2, relief=SUNKEN)
        self.ndaxFrame.grid(row=0, column=0, sticky=E + W, padx=5, pady=5)

        # Labels
        self.nl1 = Label(self.ndaxFrame, text='Trading Pair:', justify="center")
        self.nl1.grid(row=1, column=0, sticky=E + W)

        # Entries
        self.ne1 = Entry(self.ndaxFrame)
        self.ne1.grid(row=1, column=1, sticky=E + W)

        # Buttons
        Button(self.ndaxFrame, text='Get NDAX Balance', command=self.balance_callback)\
            .grid(row=0, column=0, sticky=E + W)
        Button(self.ndaxFrame, text='Get NDAX Currencies', command=self.currencies_callback) \
            .grid(row=0, column=1, sticky=E + W)
        Button(self.ndaxFrame, text='Get NDAX Deposits', command=self.deposits_callback) \
            .grid(row=0, column=3, sticky=E + W)
        Button(self.ndaxFrame, text='Get NDAX Fee', command=self.fee_callback) \
            .grid(row=0, column=4, sticky=E + W)
        Button(self.ndaxFrame, text='Get NDAX Markets', command=self.markets_callback) \
            .grid(row=0, column=5, sticky=E + W)
        Button(self.ndaxFrame, text='Get NDAX Ticker', command=self.ticker_callback) \
            .grid(row=2, column=0, columnspan=2, sticky=E + W)

        ################################################################################################################
        # Frames
        self.gridFrame = Frame(master, borderwidth=2, relief=SUNKEN)
        self.gridFrame.grid(row=1, column=0, sticky=E + W, padx=5, pady=5)

        # Labels
        self.l0 = Label(self.gridFrame, text='Grid Settings', justify="center")
        self.l0.grid(row=0, column=0, columnspan=2, sticky=E + W)
        self.l1 = Label(self.gridFrame, text='Intervals:', justify="center")
        self.l1.grid(row=1, column=0, sticky=E + W)
        self.l2 = Label(self.gridFrame, text='Amount of Crypto per Interval:', justify="center")
        self.l2.grid(row=2, column=0, sticky=E + W)
        self.l3 = Label(self.gridFrame, text='Lower Boundary:', justify="center")
        self.l3.grid(row=3, column=0, sticky=E + W)
        self.l4 = Label(self.gridFrame, text='Upper Boundary:', justify="center")
        self.l4.grid(row=4, column=0, sticky=E + W)
        self.l5 = Label(self.gridFrame, text='Number of Decimal Places:', justify="center")
        self.l5.grid(row=5, column=0, sticky=E + W)
        self.l6 = Label(self.gridFrame, text='Simulation Settings', justify="center")
        self.l6.grid(row=0, column=3, columnspan=3, sticky=E + W)
        self.l7 = Label(self.gridFrame, text='File Path:', justify="center")
        self.l7.grid(row=5, column=3, sticky=E + W)

        # Entries
        self.e1 = Entry(self.gridFrame)
        self.e1.grid(row=1, column=1, sticky=E + W)
        self.e2 = Entry(self.gridFrame)
        self.e2.grid(row=2, column=1, sticky=E + W)
        self.e3 = Entry(self.gridFrame)
        self.e3.grid(row=3, column=1, sticky=E + W)
        self.e4 = Entry(self.gridFrame)
        self.e4.grid(row=4, column=1, sticky=E + W)
        self.e5 = Entry(self.gridFrame)
        self.e5.grid(row=5, column=1, sticky=E + W)
        self.e6 = Entry(self.gridFrame)
        self.e6.grid(row=5, column=4, sticky=E + W)

        # Checkboxes
        self.var1 = IntVar()
        self.c1 = Checkbutton(self.gridFrame, text='CSV', variable=self.var1, onvalue=1, offvalue=0)
        self.c1.grid(row=5, column=5, sticky=E + W)

        # Buttons
        Button(self.gridFrame, text='Create Grid', command=self.grid_callback) \
            .grid(row=6, column=0, columnspan=2, sticky=E + W)
        Button(self.gridFrame, text='Run Simulation', command=self.simulation_callback) \
            .grid(row=6, column=3, columnspan=3, sticky=E + W)

    # Grid Button Callbacks
    def grid_callback(self):
        intervals = int(self.e1.get())
        amount = float(self.e2.get())
        min_val = float(self.e3.get())
        max_val = float(self.e4.get())
        tolerance = int(self.e5.get())
        self.create_grid(intervals, min_val, max_val, amount, tolerance)

    def simulation_callback(self):
        file_path = self.e6.get()
        if self.var1 == 1:
            self.run_paper_simulation(file_path, True)
        else:
            self.run_paper_simulation(file_path)

    def balance_callback(self):
        self.ndax.fetch_balance()

    def currencies_callback(self):
        self.ndax.fetch_currencies()

    def deposits_callback(self):
        self.ndax.fetch_deposits()

    def fee_callback(self):
        self.ndax.fetch_fee()

    def markets_callback(self):
        self.ndax.fetch_markets()

    def ticker_callback(self):
        self.ndax.fetch_ticker(self.ne1.get())

    # Complex Functions
    def create_grid(self, intervals, min_val, max_val, amount_per_int, tolerance):
        # Sample inputs: intervals=18, min_val=0.155, max_val=0.177, amount_per_int=100, tolerance=4
        self.grid = GridTrade(intervals, min_val, max_val, amount_per_int, tolerance)

    def run_paper_simulation(self, file_path, is_csv=False):
        # Sample input: file_path='data/ndax_data_08_May_22.json'
        if is_csv:
            self.grid.set_data(self.fl.load_dummy_data(file_path))  # 'data/data1.csv'
        else:
            self.grid.set_data(self.fl.load_data(file_path))
        self.grid.simulator()
