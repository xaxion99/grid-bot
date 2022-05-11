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
        self.nl0 = Label(self.ndaxFrame, text='NDAX Functions', justify="center")
        self.nl0.grid(row=0, column=0, columnspan=5, sticky=E + W)
        self.nl1 = Label(self.ndaxFrame, text='Currency:', justify="center")
        self.nl1.grid(row=3, column=0, sticky=E + W)
        self.nl2 = Label(self.ndaxFrame, text='Trading Pair:', justify="center")
        self.nl2.grid(row=3, column=2, sticky=E + W)

        # Entries
        self.ne1 = Entry(self.ndaxFrame)
        self.ne1.grid(row=3, column=1, sticky=E + W)
        self.ne1 = Entry(self.ndaxFrame)
        self.ne1.grid(row=3, column=3, sticky=E + W)

        # Buttons
        Button(self.ndaxFrame, text='Get NDAX Account', command=self.accounts_callback) \
            .grid(row=1, column=0, sticky=E + W)
        Button(self.ndaxFrame, text='Get Balance', command=self.balance_callback)\
            .grid(row=1, column=1, sticky=E + W)
        Button(self.ndaxFrame, text='Get Currencies', command=self.currencies_callback) \
            .grid(row=1, column=2, sticky=E + W)
        Button(self.ndaxFrame, text='Get Deposits', command=self.deposits_callback) \
            .grid(row=1, column=3, sticky=E + W)
        Button(self.ndaxFrame, text='Get Ledger', command=self.ledger_callback) \
            .grid(row=1, column=4, sticky=E + W)
        Button(self.ndaxFrame, text='Get Markets', command=self.markets_callback) \
            .grid(row=1, column=5, sticky=E + W)
        Button(self.ndaxFrame, text='Get Withdrawals', command=self.withdrawals_callback, state='disabled') \
            .grid(row=2, column=0, sticky=E + W)
        Button(self.ndaxFrame, text='Get Order Trades', command=self.order_trades_callback, state='disabled') \
            .grid(row=2, column=1, sticky=E + W)
        Button(self.ndaxFrame, text='Get Order Book', command=self.order_book_callback, state='disabled') \
            .grid(row=2, column=2, sticky=E + W)
        Button(self.ndaxFrame, text='Get Orders', command=self.orders_callback) \
            .grid(row=2, column=3, sticky=E + W)
        Button(self.ndaxFrame, text='Get Open Orders', command=self.open_orders_callback) \
            .grid(row=2, column=4, sticky=E + W)
        Button(self.ndaxFrame, text='Get My Trades ', command=self.my_trades_callback) \
            .grid(row=2, column=5, sticky=E + W)
        Button(self.ndaxFrame, text='Get Currency', command=self.currency_callback) \
            .grid(row=4, column=0, columnspan=2, sticky=E + W)
        Button(self.ndaxFrame, text='Get Ticker', command=self.ticker_callback) \
            .grid(row=4, column=2, columnspan=2, sticky=E + W)

        ################################################################################################################
        # Frames
        self.ohlcvFrame = Frame(master, borderwidth=2, relief=SUNKEN)
        self.ohlcvFrame.grid(row=1, column=0, sticky=E + W, padx=5, pady=5)

        # Labels
        self.ol0 = Label(self.ohlcvFrame, text='OHLC(V) Data', justify="center")
        self.ol0.grid(row=0, column=0, columnspan=2, sticky=E + W)
        self.ol1 = Label(self.ohlcvFrame, text='File Path*:', justify="center")
        self.ol1.grid(row=1, column=0, sticky=E + W)
        self.ol2 = Label(self.ohlcvFrame, text='Trading Pair*:', justify="center")
        self.ol2.grid(row=2, column=0, sticky=E + W)
        self.ol3 = Label(self.ohlcvFrame, text='Time Frequency*:', justify="center")
        self.ol3.grid(row=3, column=0, sticky=E + W)
        self.ol4 = Label(self.ohlcvFrame, text='Since (UNIX time)*:', justify="center")
        self.ol4.grid(row=4, column=0, sticky=E + W)

        # Entries
        self.oe1 = Entry(self.ohlcvFrame)
        self.oe1.grid(row=1, column=1, sticky=E + W)
        self.oe2 = Entry(self.ohlcvFrame)
        self.oe2.grid(row=2, column=1, sticky=E + W)
        self.oe3 = Entry(self.ohlcvFrame)
        self.oe3.grid(row=3, column=1, sticky=E + W)
        self.oe4 = Entry(self.ohlcvFrame)
        self.oe4.grid(row=4, column=1, sticky=E + W)

        # Buttons
        Button(self.ohlcvFrame, text='Get NDAX OHLC(V)', command=self.ohlcv_callback) \
            .grid(row=5, column=0, columnspan=2, sticky=E + W)

        ################################################################################################################
        # Frames
        self.gridFrame = Frame(master, borderwidth=2, relief=SUNKEN)
        self.gridFrame.grid(row=2, column=0, sticky=E + W, padx=5, pady=5)

        # Labels
        self.l0 = Label(self.gridFrame, text='Grid Settings', justify="center")
        self.l0.grid(row=0, column=0, columnspan=3, sticky=E + W)
        self.l1 = Label(self.gridFrame, text='Intervals*:', justify="center")
        self.l1.grid(row=1, column=0, sticky=E + W)
        self.l2 = Label(self.gridFrame, text='Amount of Crypto per Interval*:', justify="center")
        self.l2.grid(row=2, column=0, sticky=E + W)
        self.l3 = Label(self.gridFrame, text='Lower Boundary*:', justify="center")
        self.l3.grid(row=3, column=0, sticky=E + W)
        self.l4 = Label(self.gridFrame, text='Upper Boundary*:', justify="center")
        self.l4.grid(row=4, column=0, sticky=E + W)
        self.l5 = Label(self.gridFrame, text='Number of Decimal Places*:', justify="center")
        self.l5.grid(row=5, column=0, sticky=E + W)

        self.l6 = Label(self.gridFrame, text='-', justify="center")
        self.l6.grid(row=1, column=2, sticky=E + W)
        self.l7 = Label(self.gridFrame, text='-', justify="center")
        self.l7.grid(row=2, column=2, sticky=E + W)
        self.l8 = Label(self.gridFrame, text='-', justify="center")
        self.l8.grid(row=3, column=2, sticky=E + W)
        self.l9 = Label(self.gridFrame, text='-', justify="center")
        self.l9.grid(row=4, column=2, sticky=E + W)
        self.l10 = Label(self.gridFrame, text='-', justify="center")
        self.l10.grid(row=5, column=2, sticky=E + W)

        self.l11 = Label(self.gridFrame, text='Simulation Settings', justify="center")
        self.l11.grid(row=0, column=3, columnspan=3, sticky=E + W)
        self.l12 = Label(self.gridFrame, text='Crypto:', justify="center")
        self.l12.grid(row=3, column=3, sticky=E + W)
        self.l13 = Label(self.gridFrame, text='Fiat:', justify="center")
        self.l13.grid(row=4, column=3, sticky=E + W)
        self.l14 = Label(self.gridFrame, text='File Path*:', justify="center")
        self.l14.grid(row=5, column=3, sticky=E + W)

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
        self.e6.grid(row=3, column=4, sticky=E + W)
        self.e7 = Entry(self.gridFrame)
        self.e7.grid(row=4, column=4, sticky=E + W)
        self.e8 = Entry(self.gridFrame)
        self.e8.grid(row=5, column=4, sticky=E + W)

        # Checkboxes
        self.var1 = IntVar()
        self.c1 = Checkbutton(self.gridFrame, text='CSV', variable=self.var1, onvalue=1, offvalue=0)
        self.c1.grid(row=5, column=5, sticky=E + W)

        # Buttons
        self.b1 = Button(self.gridFrame, text='Create Grid', command=self.grid_callback)
        self.b1.grid(row=6, column=0, columnspan=3, sticky=E + W)
        self.b2 = Button(self.gridFrame, text='Run Simulation', command=self.simulation_callback, state='disabled')
        self.b2.grid(row=6, column=3, columnspan=3, sticky=E + W)

    # Grid Button Callbacks
    def grid_callback(self):
        intervals = int(self.e1.get())
        amount = float(self.e2.get())
        min_val = float(self.e3.get())
        max_val = float(self.e4.get())
        tolerance = int(self.e5.get())
        self.create_grid(intervals, min_val, max_val, amount, tolerance)
        self.l6.config(text=str(intervals))
        self.l7.config(text=str(amount))
        self.l8.config(text=str(min_val))
        self.l9.config(text=str(max_val))
        self.l10.config(text=str(tolerance))
        self.b2['state'] = 'normal'

    def simulation_callback(self):
        file_path = self.e8.get()
        if self.var1 == 1:
            self.run_paper_simulation(file_path, True)
        else:
            self.run_paper_simulation(file_path)

    # NDAX Button Callbacks
    def accounts_callback(self):
        self.ndax.fetch_accounts()

    def balance_callback(self):
        self.ndax.fetch_balance()

    def currency_callback(self):
        self.ndax.fetch_currency('BTC')

    def currencies_callback(self):
        self.ndax.fetch_currencies()

    def deposits_callback(self):
        self.ndax.fetch_deposits()

    def ledger_callback(self):
        self.ndax.fetch_ledger()

    def markets_callback(self):
        self.ndax.fetch_markets()

    def my_trades_callback(self):
        self.ndax.fetch_my_trades()

    def orders_callback(self):
        self.ndax.fetch_orders()

    def open_orders_callback(self):
        # self.ndax.create_order('DOGE/CAD', 'limit', 1, 10, 0.50)
        self.ndax.fetch_open_orders()

    def order_book_callback(self):
        self.ndax.fetch_order_book()

    def order_trades_callback(self):
        self.ndax.fetch_order_trades()

    def ticker_callback(self):
        self.ndax.fetch_ticker(self.ne1.get())

    def withdrawals_callback(self):
        self.ndax.fetch_withdrawals()

    # OHLC(V) Button Callback
    def ohlcv_callback(self):
        file_path = self.oe1.get()
        pair = self.oe2.get()
        tf = self.oe3.get()
        since = int(self.oe4.get())
        self.ndax.fetch_ohlcv(file_path=file_path, pair=pair, tf=tf, since=since)

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
        crypto = self.e6.get()
        fiat = self.e7.get()
        if crypto == '' and fiat == '':
            self.grid.simulator()
        elif crypto == '' and fiat != '':
            self.grid.simulator(fiat=float(fiat))
        elif crypto != '' and fiat == '':
            self.grid.simulator(crypto=float(crypto))
        else:
            self.grid.simulator(fiat=float(fiat), crypto=float(crypto))
