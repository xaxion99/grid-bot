import statistics
from exchange import Exchange
from file_loader import FileLoader
from grid import GridTrade
from strategy import Strategy
from tkinter import *


class GUI:
    def __init__(self, master, login):
        self.master = master
        self.ndax = Exchange(login)
        self.fl = FileLoader()
        self.market_strategies = ['Ranging', 'Trending']
        self.time_frames = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d', '1w', '1M', '4M']

        # Setup the master window
        master.title("NDAX Grid Trading Bot")
        # master.wm_iconbitmap('Icons/logo_large.ico')  # Add logo to top bar
        # master.resizable(height = None, width = None)
        master.resizable(0, 0)  # Make window not resizable (resizing is broken atm)
        
        ################################################################################################################
        # Menus
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # Account Menu
        account_menu = Menu(menu, tearoff=False)
        account_menu.add_command(label="Info", command=self.accounts_callback)
        account_menu.add_command(label="Balances", command=self.balance_callback)
        account_menu.add_command(label="Deposits", command=self.deposits_callback)
        account_menu.add_command(label="Withdrawals", command=self.withdrawals_callback)
        account_menu.add_command(label="Ledger", command=self.ledger_callback)
        account_menu.add_command(label="My Trade History", command=self.my_trades_callback)
        menu.add_cascade(label="Account", menu=account_menu)

        # Order Menu
        order_menu = Menu(menu, tearoff=False)
        order_menu.add_command(label="All Orders", command=self.orders_callback)
        order_menu.add_command(label="Open Orders", command=self.open_orders_callback)
        order_menu.add_command(label="Order Book", command=self.order_book_callback, state='disabled')
        order_menu.add_command(label="Open Trades", command=self.order_trades_callback, state='disabled')
        menu.add_cascade(label="Order", menu=order_menu)

        # NDAX Menu
        ndax_menu = Menu(menu, tearoff=False)
        # Currency Submenu
        currency_menu = Menu(ndax_menu, tearoff=False)
        curs = self.ndax.fetch_currencies()
        for c in curs:
            currency_menu.add_command(label=c, command=lambda i=c: self.currency_callback(i))
        ndax_menu.add_cascade(label='Currency', menu=currency_menu)
        ndax_menu.add_command(label="Currencies", command=self.currencies_callback)
        # Market Submenu
        market_menu = Menu(ndax_menu, tearoff=False)
        tps = self.ndax.fetch_trading_pairs()
        for tp in tps:
            market_menu.add_command(label=tp, command=lambda i=tp: self.market_callback(i))
        ndax_menu.add_cascade(label='Market', menu=market_menu)
        ndax_menu.add_command(label="Markets", command=self.markets_callback)
        # Ticker Submenu
        ticker_menu = Menu(ndax_menu, tearoff=False)
        for tp in tps:
            ticker_menu.add_command(label=tp, command=lambda i=tp: self.ticker_callback(i))
        ndax_menu.add_cascade(label='Check Ticker', menu=ticker_menu)
        menu.add_cascade(label="NDAX", menu=ndax_menu)

        ################################################################################################################
        # OHLC(V) Frame
        self.ohlcvFrame = Frame(self.master, borderwidth=2, relief=SUNKEN)
        self.ohlcvFrame.grid(row=0, column=0, sticky=E + W, padx=5, pady=5)

        # Labels
        self.ol0 = Label(self.ohlcvFrame, text='OHLC(V) Data', justify="center")
        self.ol0.grid(row=0, column=0, columnspan=4, sticky=E + W)
        self.ol1 = Label(self.ohlcvFrame, text='File Path*:', justify="center")
        self.ol1.grid(row=1, column=0, sticky=E + W)
        self.ol2 = Label(self.ohlcvFrame, text='Trading Pair*:', justify="center")
        self.ol2.grid(row=2, column=0, sticky=E + W)
        self.ol3 = Label(self.ohlcvFrame, text='Time Frequency*:', justify="center")
        self.ol3.grid(row=3, column=0, sticky=E + W)
        self.ol4 = Label(self.ohlcvFrame, text='Since (UNIX time):', justify="center")
        self.ol4.grid(row=4, column=0, sticky=E + W)
        self.ol5 = Label(self.ohlcvFrame, text='Limit (Data Points):', justify="center")
        self.ol5.grid(row=5, column=0, sticky=E + W)
        self.ol6 = Label(self.ohlcvFrame, text='Trading Pair:', justify="center")
        self.ol6.grid(row=1, column=2, sticky=E + W)
        self.ol7 = Label(self.ohlcvFrame, text='Min Value:', justify="center")
        self.ol7.grid(row=2, column=2, sticky=E + W)
        self.ol8 = Label(self.ohlcvFrame, text='Mean Value:', justify="center")
        self.ol8.grid(row=3, column=2, sticky=E + W)
        self.ol9 = Label(self.ohlcvFrame, text='Median Value:', justify="center")
        self.ol9.grid(row=4, column=2, sticky=E + W)
        self.ol10 = Label(self.ohlcvFrame, text='Mid Value:', justify="center")
        self.ol10.grid(row=5, column=2, sticky=E + W)
        self.ol11 = Label(self.ohlcvFrame, text='Max Value:', justify="center")
        self.ol11.grid(row=6, column=2, sticky=E + W)
        self.ol12 = Label(self.ohlcvFrame, text='-', justify="center")
        self.ol12.grid(row=1, column=3, sticky=E + W)
        self.ol13 = Label(self.ohlcvFrame, text='-', justify="center")
        self.ol13.grid(row=2, column=3, sticky=E + W)
        self.ol14 = Label(self.ohlcvFrame, text='-', justify="center")
        self.ol14.grid(row=3, column=3, sticky=E + W)
        self.ol15 = Label(self.ohlcvFrame, text='-', justify="center")
        self.ol15.grid(row=4, column=3, sticky=E + W)
        self.ol16 = Label(self.ohlcvFrame, text='-', justify="center")
        self.ol16.grid(row=5, column=3, sticky=E + W)
        self.ol17 = Label(self.ohlcvFrame, text='-', justify="center")
        self.ol17.grid(row=6, column=3, sticky=E + W)

        # Dropdown Menu
        self.menu1 = StringVar()
        self.menu1.set("Select a trading pair")
        self.od1 = OptionMenu(self.ohlcvFrame, self.menu1, *self.ndax.fetch_trading_pairs())
        self.od1.grid(row=2, column=1, sticky=E + W)
        self.menu2 = StringVar()
        self.menu2.set("Select a time frequency")
        self.od2 = OptionMenu(self.ohlcvFrame, self.menu2, *self.time_frames)
        self.od2.grid(row=3, column=1, sticky=E + W)

        # Entries
        self.oe1 = Entry(self.ohlcvFrame)
        self.oe1.insert(0, 'data/ohlcv_data.json')
        self.oe1.grid(row=1, column=1, sticky=E + W)
        self.oe2 = Entry(self.ohlcvFrame)
        self.oe2.grid(row=4, column=1, sticky=E + W)
        self.oe3 = Entry(self.ohlcvFrame)
        self.oe3.grid(row=5, column=1, sticky=E + W)

        # Buttons
        Button(self.ohlcvFrame, text='Get NDAX OHLC(V)', command=self.ohlcv_callback) \
            .grid(row=6, column=0, columnspan=2, sticky=E + W)

        ################################################################################################################
        # Grid Frame
        self.gridFrame = Frame(master, borderwidth=2, relief=SUNKEN)
        self.gridFrame.grid(row=1, column=0, sticky=E + W, padx=5, pady=5)

        # Labels
        self.gl0 = Label(self.gridFrame, text='Grid Settings', justify="center")
        self.gl0.grid(row=0, column=0, columnspan=3, sticky=E + W)
        self.gl1 = Label(self.gridFrame, text='Intervals (Even)*:', justify="center")
        self.gl1.grid(row=1, column=0, sticky=E + W)
        self.gl2 = Label(self.gridFrame, text='Amount of Crypto per Interval*:', justify="center")
        self.gl2.grid(row=2, column=0, sticky=E + W)
        self.gl3 = Label(self.gridFrame, text='Lower Boundary*:', justify="center")
        self.gl3.grid(row=3, column=0, sticky=E + W)
        self.gl4 = Label(self.gridFrame, text='Upper Boundary*:', justify="center")
        self.gl4.grid(row=4, column=0, sticky=E + W)
        self.gl5 = Label(self.gridFrame, text='Number of Decimal Places*:', justify="center")
        self.gl5.grid(row=5, column=0, sticky=E + W)
        self.gl6 = Label(self.gridFrame, text='-', justify="center")
        self.gl6.grid(row=1, column=2, sticky=E + W)
        self.gl7 = Label(self.gridFrame, text='-', justify="center")
        self.gl7.grid(row=2, column=2, sticky=E + W)
        self.gl8 = Label(self.gridFrame, text='-', justify="center")
        self.gl8.grid(row=3, column=2, sticky=E + W)
        self.gl9 = Label(self.gridFrame, text='-', justify="center")
        self.gl9.grid(row=4, column=2, sticky=E + W)
        self.gl10 = Label(self.gridFrame, text='-', justify="center")
        self.gl10.grid(row=5, column=2, sticky=E + W)

        # Entries
        self.ge1 = Entry(self.gridFrame)
        self.ge1.insert(0, '20')
        self.ge1.grid(row=1, column=1, sticky=E + W)
        self.ge2 = Entry(self.gridFrame)
        self.ge2.grid(row=2, column=1, sticky=E + W)
        self.ge3 = Entry(self.gridFrame)
        self.ge3.grid(row=3, column=1, sticky=E + W)
        self.ge4 = Entry(self.gridFrame)
        self.ge4.grid(row=4, column=1, sticky=E + W)
        self.ge5 = Entry(self.gridFrame)
        self.ge5.insert(0, '4')
        self.ge5.grid(row=5, column=1, sticky=E + W)

        # Buttons
        Button(self.gridFrame, text='Create Grid', command=self.grid_callback)\
            .grid(row=6, column=0, columnspan=3, sticky=E + W)

        ################################################################################################################
        # Simulation Frame
        self.simulationFrame = Frame(master, borderwidth=2, relief=SUNKEN)
        self.simulationFrame.grid(row=2, column=0, sticky=E + W, padx=5, pady=5)

        # Labels
        self.sl1 = Label(self.simulationFrame, text='Simulation Settings', justify="center")
        self.sl1.grid(row=0, column=0, columnspan=3, sticky=E + W)
        self.sl2 = Label(self.simulationFrame, text='Market Type*:', justify="center")
        self.sl2.grid(row=1, column=0, sticky=E + W)
        self.sl3 = Label(self.simulationFrame, text='Crypto (Default: 1000):', justify="center")
        self.sl3.grid(row=2, column=0, sticky=E + W)
        self.sl4 = Label(self.simulationFrame, text='Fiat (Default: 100):', justify="center")
        self.sl4.grid(row=3, column=0, sticky=E + W)
        self.sl5 = Label(self.simulationFrame, text='File Path*:', justify="center")
        self.sl5.grid(row=4, column=0, sticky=E + W)

        # Entries
        self.se1 = Entry(self.simulationFrame)
        self.se1.grid(row=2, column=1, sticky=E + W)
        self.se2 = Entry(self.simulationFrame)
        self.se2.grid(row=3, column=1, sticky=E + W)
        self.se3 = Entry(self.simulationFrame)
        self.se3.insert(0, 'data/ohlcv_data.json')
        self.se3.grid(row=4, column=1, sticky=E + W)

        # Dropdowns
        self.menu3 = StringVar()
        self.menu3.set("Select a market type")
        self.sd1 = OptionMenu(self.simulationFrame, self.menu3, *self.market_strategies)
        self.sd1.grid(row=1, column=1, sticky=E + W)

        # Checkboxes
        self.var1 = IntVar()
        self.sc1 = Checkbutton(self.simulationFrame, text='CSV', variable=self.var1, onvalue=1, offvalue=0)
        self.sc1.grid(row=4, column=2, sticky=E + W)

        # Button
        self.b1 = Button(self.simulationFrame, text='Run Simulation', command=self.simulation_callback,
                         state='disabled')
        self.b1.grid(row=5, column=0, columnspan=3, sticky=E + W)

    ####################################################################################################################
    # NDAX Button Callbacks
    def accounts_callback(self):
        self.ndax.fetch_accounts()

    def balance_callback(self):
        self.ndax.fetch_balance()

    def currency_callback(self, c):
        self.ndax.fetch_currency(c)

    def currencies_callback(self):
        self.ndax.fetch_currencies()

    def deposits_callback(self):
        self.ndax.fetch_deposits()

    def ledger_callback(self):
        self.ndax.fetch_ledger()

    def market_callback(self, tp):
        self.ndax.fetch_market(tp)

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

    def ticker_callback(self, tp):
        self.ndax.fetch_ticker(tp)

    def withdrawals_callback(self):
        self.ndax.fetch_withdrawals()

    ####################################################################################################################
    # OHLC(V) Button Callback
    def ohlcv_callback(self):
        file_path = self.oe1.get()
        pair = self.menu1.get()
        tf = self.menu2.get()
        if self.oe2.get() == '':
            since = None
        else:
            since = int(self.oe2.get())
        if self.oe3.get() == '':
            limit = None
        else:
            limit = int(self.oe3.get())
        d = self.ndax.fetch_ohlcv(file_path=file_path, pair=pair, tf=tf, since=since, limit=limit)
        self.ol12.config(text=pair)
        self.ol13.config(text=str(min(d.values())))
        self.ol14.config(text=str(round(statistics.mean(d.values()), 8)))
        self.ol15.config(text=str(round(statistics.median(d.values()), 8)))
        self.ol16.config(text=str(round((min(d.values()) + max(d.values())) / 2, 8)))
        self.ol17.config(text=str(max(d.values())))

    ####################################################################################################################
    # Grid Button Callbacks
    def grid_callback(self):
        if int(self.ge1.get()) % 2 != 0:
            intervals = int(self.ge1.get()) - 1
        else:
            intervals = int(self.ge1.get())
        amount = float(self.ge2.get())
        min_val = float(self.ge3.get())
        max_val = float(self.ge4.get())
        tolerance = int(self.ge5.get())
        self.create_grid(intervals, min_val, max_val, amount, tolerance)
        self.gl6.config(text=str(intervals))
        self.gl7.config(text=str(amount))
        self.gl8.config(text=str(min_val))
        self.gl9.config(text=str(max_val))
        self.gl10.config(text=str(tolerance))
        self.b1['state'] = 'normal'

    def simulation_callback(self):
        file_path = self.se3.get()
        if self.var1 == 1:
            self.run_paper_simulation(file_path, True)
        else:
            self.run_paper_simulation(file_path)

    ####################################################################################################################
    # Complex Functions
    def create_grid(self, intervals, min_val, max_val, amount_per_int, tolerance):
        # Sample inputs: intervals=18, min_val=0.155, max_val=0.177, amount_per_int=100, tolerance=4
        self.grid = GridTrade(intervals, min_val, max_val, amount_per_int, tolerance, self.ndax)

    def run_paper_simulation(self, file_path, is_csv=False):
        # Sample input: file_path='data/ndax_data_08_May_22.json'
        if is_csv:
            self.grid.set_data(self.fl.load_dummy_data(file_path))  # 'data/data1.csv'
        else:
            self.grid.set_data(self.fl.load_data(file_path))
        s = Strategy(self.grid, self.ndax)
        ms = self.menu3.get()
        crypto = self.se1.get()
        fiat = self.se2.get()
        if ms == 'Ranging':
            if crypto == '' and fiat == '':
                s.range_simulator()
            elif crypto == '' and fiat != '':
                s.range_simulator(fiat=float(fiat))
            elif crypto != '' and fiat == '':
                s.range_simulator(crypto=float(crypto))
            else:
                s.range_simulator(fiat=float(fiat), crypto=float(crypto))
        elif ms == 'Trending':
            if crypto == '' and fiat == '':
                s.trend_simulator()
            elif crypto == '' and fiat != '':
                s.trend_simulator(fiat=float(fiat))
            elif crypto != '' and fiat == '':
                s.trend_simulator(crypto=float(crypto))
            else:
                s.trend_simulator(fiat=float(fiat), crypto=float(crypto))
