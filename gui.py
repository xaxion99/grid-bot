import matplotlib.dates as md
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import statistics
from datetime import datetime
from exchange import Exchange
from file_loader import FileLoader
from grid import GridTrade
from livethread import LiveThread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from strategy import Strategy
from tkinter import *
from tkinter import font


class GUI:
    def __init__(self, master, login):
        self.master = master
        self.ndax = Exchange(login)
        self.fl = FileLoader()
        self.live_thread = None
        self.market_strategies = ['Ranging', 'Trending']
        self.types_array = ['candle', 'line', 'ohlc', 'pnf', 'renko']
        self.time_frames = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d', '1w', '1M', '4M']

        # Setup the master window
        self.master.title("NDAX Grid Trading Bot")
        # master.wm_iconbitmap('Icons/logo_large.ico')  # Add logo to top bar
        self.master.resizable(1, 1)  # Make window not resizable (resizing is broken atm)

        # Setup configurable variables
        self.font_header = font.Font(self.master, family='Times New Roman', size=20, weight='bold')
        self.font = font.Font(self.master, family='Times New Roman', size=16)
        self.title = 'OHLC(V) Graph'
        self.style = 'default'
        self.type = 'candle'
        
        ################################################################################################################
        # Menus
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # File Menu
        file_menu = Menu(menu, tearoff=False)
        file_menu.add_command(label="Exit", command=self.exit_callback, font=self.font)
        menu.add_cascade(label="File", menu=file_menu, font=self.font_header)

        # Account Menu
        account_menu = Menu(menu, tearoff=False)
        account_menu.add_command(label="Info", command=self.accounts_callback, font=self.font)
        account_menu.add_command(label="Balances", command=self.balance_callback, font=self.font)
        account_menu.add_command(label="Deposits", command=self.deposits_callback, font=self.font)
        account_menu.add_command(label="Withdrawals", command=self.withdrawals_callback, font=self.font)
        account_menu.add_command(label="Ledger", command=self.ledger_callback, font=self.font)
        account_menu.add_command(label="My Trade History", command=self.my_trades_callback, font=self.font)
        menu.add_cascade(label="Account", menu=account_menu, font=self.font_header)

        # Order Menu
        order_menu = Menu(menu, tearoff=False)
        order_menu.add_command(label="All Orders", command=self.orders_callback, font=self.font)
        order_menu.add_command(label="Open Orders", command=self.open_orders_callback, font=self.font)
        order_menu.add_command(label="Order Book", command=self.order_book_callback, font=self.font, state='disabled')
        order_menu.add_command(label="Open Trades", command=self.order_trades_callback, font=self.font,
                               state='disabled')
        menu.add_cascade(label="Order", menu=order_menu, font=self.font_header)

        # NDAX Menu
        ndax_menu = Menu(menu, tearoff=False)
        # Currency Submenu
        currency_menu = Menu(ndax_menu, tearoff=False)
        curs = self.ndax.fetch_currencies()
        for c in curs:
            currency_menu.add_command(label=c, command=lambda i=c: self.currency_callback(i), font=self.font)
        ndax_menu.add_cascade(label='Currency', menu=currency_menu, font=self.font)
        ndax_menu.add_command(label="Currencies", command=self.currencies_callback, font=self.font)
        # Market Submenu
        market_menu = Menu(ndax_menu, tearoff=False)
        tps = self.ndax.fetch_trading_pairs()
        for tp in tps:
            market_menu.add_command(label=tp, command=lambda i=tp: self.market_callback(i), font=self.font)
        ndax_menu.add_cascade(label='Market', menu=market_menu, font=self.font)
        ndax_menu.add_command(label="Markets", command=self.markets_callback, font=self.font)
        # Ticker Submenu
        ticker_menu = Menu(ndax_menu, tearoff=False)
        for tp in tps:
            ticker_menu.add_command(label=tp, command=lambda i=tp: self.ticker_callback(i), font=self.font)
        ndax_menu.add_cascade(label='Check Ticker', menu=ticker_menu, font=self.font)
        menu.add_cascade(label="NDAX", menu=ndax_menu, font=self.font_header)

        # Plot Menu
        plot_menu = Menu(menu, tearoff=False)
        # Style Submenu
        style_menu = Menu(plot_menu, tearoff=False)
        styles = mpf.available_styles()
        for s in styles:
            style_menu.add_command(label=s, command=lambda i=s: self.style_callback(i), font=self.font)
        plot_menu.add_cascade(label='Style', menu=style_menu, font=self.font)
        # Type Submenu
        type_menu = Menu(plot_menu, tearoff=False)
        types = self.types_array
        for t in types:
            type_menu.add_command(label=t, command=lambda i=t: self.type_callback(i), font=self.font)
        plot_menu.add_cascade(label='Type', menu=type_menu, font=self.font)
        menu.add_cascade(label="Plot", menu=plot_menu, font=self.font_header)

        ################################################################################################################
        # Master Frames
        self.topFrame = Frame(self.master, borderwidth=2, relief=SUNKEN)
        self.topFrame.pack(side='top', fill='both', expand=True)

        self.bottomFrame = Frame(self.master, borderwidth=2, relief=SUNKEN)
        self.bottomFrame.pack(side='top', fill='both', expand=True)
        self.bottomFrame.rowconfigure(0, weight=1)
        self.bottomFrame.columnconfigure(0, weight=1)
        self.bottomFrame.columnconfigure(1, weight=1)
        self.bottomFrame.columnconfigure(2, weight=1)
        self.bottomFrame.columnconfigure(3, weight=1)

        ################################################################################################################
        # OHLC(V) Frame
        self.ohlcvFrame = Frame(self.bottomFrame, borderwidth=2, relief=SUNKEN)
        self.ohlcvFrame.grid(row=0, column=0, sticky=N+E+S+W, padx=5, pady=5)
        self.ohlcvFrame.rowconfigure(0, weight=1)
        self.ohlcvFrame.rowconfigure(1, weight=1)
        self.ohlcvFrame.rowconfigure(2, weight=1)
        self.ohlcvFrame.rowconfigure(3, weight=1)
        self.ohlcvFrame.rowconfigure(4, weight=1)
        self.ohlcvFrame.rowconfigure(5, weight=1)
        self.ohlcvFrame.rowconfigure(6, weight=1)
        self.ohlcvFrame.columnconfigure(0, weight=1)
        self.ohlcvFrame.columnconfigure(1, weight=1)
        self.ohlcvFrame.columnconfigure(2, weight=1)
        self.ohlcvFrame.columnconfigure(3, weight=1)

        # Labels
        self.ol0 = Label(self.ohlcvFrame, text='OHLC(V) Historical Data', justify="center", font=self.font_header)
        self.ol0.grid(row=0, column=0, columnspan=4, sticky=N+E+S+W)
        self.ol1 = Label(self.ohlcvFrame, text='File Path*:', justify="center", font=self.font)
        self.ol1.grid(row=1, column=0, sticky=N+E+S+W)
        self.ol2 = Label(self.ohlcvFrame, text='Trading Pair*:', justify="center", font=self.font)
        self.ol2.grid(row=2, column=0, sticky=N+E+S+W)
        self.ol3 = Label(self.ohlcvFrame, text='Time Frequency*:', justify="center", font=self.font)
        self.ol3.grid(row=3, column=0, sticky=N+E+S+W)
        self.ol4 = Label(self.ohlcvFrame, text='Since (UNIX time):', justify="center", font=self.font)
        self.ol4.grid(row=4, column=0, sticky=N+E+S+W)
        self.ol5 = Label(self.ohlcvFrame, text='Limit (Data Points):', justify="center", font=self.font)
        self.ol5.grid(row=5, column=0, sticky=N+E+S+W)
        self.ol6 = Label(self.ohlcvFrame, text='Trading Pair:', justify="center", font=self.font)
        self.ol6.grid(row=1, column=2, sticky=N+E+S+W)
        self.ol7 = Label(self.ohlcvFrame, text='Min Value:', justify="center", font=self.font)
        self.ol7.grid(row=2, column=2, sticky=N+E+S+W)
        self.ol8 = Label(self.ohlcvFrame, text='Mean Value:', justify="center", font=self.font)
        self.ol8.grid(row=3, column=2, sticky=N+E+S+W)
        self.ol9 = Label(self.ohlcvFrame, text='Median Value:', justify="center", font=self.font)
        self.ol9.grid(row=4, column=2, sticky=N+E+S+W)
        self.ol10 = Label(self.ohlcvFrame, text='Mid Value:', justify="center", font=self.font)
        self.ol10.grid(row=5, column=2, sticky=N+E+S+W)
        self.ol11 = Label(self.ohlcvFrame, text='Max Value:', justify="center", font=self.font)
        self.ol11.grid(row=6, column=2, sticky=N+E+S+W)
        self.ol12 = Label(self.ohlcvFrame, text='-', justify="center", font=self.font)
        self.ol12.grid(row=1, column=3, sticky=N+E+S+W)
        self.ol13 = Label(self.ohlcvFrame, text='-', justify="center", font=self.font)
        self.ol13.grid(row=2, column=3, sticky=N+E+S+W)
        self.ol14 = Label(self.ohlcvFrame, text='-', justify="center", font=self.font)
        self.ol14.grid(row=3, column=3, sticky=N+E+S+W)
        self.ol15 = Label(self.ohlcvFrame, text='-', justify="center", font=self.font)
        self.ol15.grid(row=4, column=3, sticky=N+E+S+W)
        self.ol16 = Label(self.ohlcvFrame, text='-', justify="center", font=self.font)
        self.ol16.grid(row=5, column=3, sticky=N+E+S+W)
        self.ol17 = Label(self.ohlcvFrame, text='-', justify="center", font=self.font)
        self.ol17.grid(row=6, column=3, sticky=N+E+S+W)

        # Dropdown Menu
        self.menu1 = StringVar()
        self.menu1.set("Select a trading pair")
        self.od1 = OptionMenu(self.ohlcvFrame, self.menu1, *self.ndax.fetch_trading_pairs())
        self.od1.config(font=self.font)
        menu = self.ohlcvFrame.nametowidget(self.od1.menuname)
        menu.config(font=self.font)
        self.od1.grid(row=2, column=1, sticky=N+E+S+W)
        self.menu2 = StringVar()
        self.menu2.set("Select a time frequency")
        self.od2 = OptionMenu(self.ohlcvFrame, self.menu2, *self.time_frames)
        self.od2.config(font=self.font)
        menu = self.ohlcvFrame.nametowidget(self.od2.menuname)
        menu.config(font=self.font)
        self.od2.grid(row=3, column=1, sticky=N+E+S+W)

        # Entries
        self.oe1 = Entry(self.ohlcvFrame, font=self.font)
        self.oe1.insert(0, 'data/ohlcv_data.json')
        self.oe1.grid(row=1, column=1, sticky=N+E+S+W)
        self.oe2 = Entry(self.ohlcvFrame, font=self.font)
        self.oe2.grid(row=4, column=1, sticky=N+E+S+W)
        self.oe3 = Entry(self.ohlcvFrame, font=self.font)
        self.oe3.grid(row=5, column=1, sticky=N+E+S+W)

        # Buttons
        Button(self.ohlcvFrame, text='Get NDAX OHLC(V)', command=self.ohlcv_callback, font=self.font) \
            .grid(row=6, column=0, columnspan=2, sticky=N+E+S+W)

        ################################################################################################################
        # Grid Frame
        self.gridFrame = Frame(self.bottomFrame, borderwidth=2, relief=SUNKEN)
        self.gridFrame.grid(row=0, column=1, sticky=N+E+S+W, padx=5, pady=5)
        self.gridFrame.rowconfigure(0, weight=1)
        self.gridFrame.rowconfigure(1, weight=1)
        self.gridFrame.rowconfigure(2, weight=1)
        self.gridFrame.rowconfigure(3, weight=1)
        self.gridFrame.rowconfigure(4, weight=1)
        self.gridFrame.rowconfigure(5, weight=1)
        self.gridFrame.rowconfigure(6, weight=1)
        self.gridFrame.columnconfigure(0, weight=1)
        self.gridFrame.columnconfigure(1, weight=1)
        self.gridFrame.columnconfigure(2, weight=1)

        # Labels
        self.gl0 = Label(self.gridFrame, text='Grid Settings', justify="center", font=self.font_header)
        self.gl0.grid(row=0, column=0, columnspan=3, sticky=N+E+S+W)
        self.gl1 = Label(self.gridFrame, text='Intervals (Even)*:', justify="center", font=self.font)
        self.gl1.grid(row=1, column=0, sticky=N+E+S+W)
        self.gl2 = Label(self.gridFrame, text='Amount of Crypto per Interval*:', justify="center", font=self.font)
        self.gl2.grid(row=2, column=0, sticky=N+E+S+W)
        self.gl3 = Label(self.gridFrame, text='Lower Boundary*:', justify="center", font=self.font)
        self.gl3.grid(row=3, column=0, sticky=N+E+S+W)
        self.gl4 = Label(self.gridFrame, text='Upper Boundary*:', justify="center", font=self.font)
        self.gl4.grid(row=4, column=0, sticky=N+E+S+W)
        self.gl5 = Label(self.gridFrame, text='Number of Decimal Places*:', justify="center", font=self.font)
        self.gl5.grid(row=5, column=0, sticky=N+E+S+W)
        self.gl6 = Label(self.gridFrame, text='-', justify="center", font=self.font)
        self.gl6.grid(row=1, column=2, sticky=N+E+S+W)
        self.gl7 = Label(self.gridFrame, text='-', justify="center", font=self.font)
        self.gl7.grid(row=2, column=2, sticky=N+E+S+W)
        self.gl8 = Label(self.gridFrame, text='-', justify="center", font=self.font)
        self.gl8.grid(row=3, column=2, sticky=N+E+S+W)
        self.gl9 = Label(self.gridFrame, text='-', justify="center", font=self.font)
        self.gl9.grid(row=4, column=2, sticky=N+E+S+W)
        self.gl10 = Label(self.gridFrame, text='-', justify="center", font=self.font)
        self.gl10.grid(row=5, column=2, sticky=N+E+S+W)

        # Entries
        self.ge1 = Entry(self.gridFrame, font=self.font)
        self.ge1.insert(0, '20')
        self.ge1.grid(row=1, column=1, sticky=N+E+S+W)
        self.ge2 = Entry(self.gridFrame, font=self.font)
        self.ge2.grid(row=2, column=1, sticky=N+E+S+W)
        self.ge3 = Entry(self.gridFrame, font=self.font)
        self.ge3.grid(row=3, column=1, sticky=N+E+S+W)
        self.ge4 = Entry(self.gridFrame, font=self.font)
        self.ge4.grid(row=4, column=1, sticky=N+E+S+W)
        self.ge5 = Entry(self.gridFrame, font=self.font)
        self.ge5.insert(0, '4')
        self.ge5.grid(row=5, column=1, sticky=N+E+S+W)

        # Buttons
        Button(self.gridFrame, text='Create Grid', command=self.grid_callback, font=self.font) \
            .grid(row=6, column=0, columnspan=3, sticky=N+E+S+W)

        ################################################################################################################
        # Simulation Frame
        self.simulationFrame = Frame(self.bottomFrame, borderwidth=2, relief=SUNKEN)
        self.simulationFrame.grid(row=0, column=2, sticky=N+E+S+W, padx=5, pady=5)
        self.simulationFrame.rowconfigure(0, weight=1)
        self.simulationFrame.rowconfigure(1, weight=1)
        self.simulationFrame.rowconfigure(2, weight=1)
        self.simulationFrame.rowconfigure(3, weight=1)
        self.simulationFrame.rowconfigure(4, weight=1)
        self.simulationFrame.rowconfigure(5, weight=1)
        self.simulationFrame.columnconfigure(0, weight=1)
        self.simulationFrame.columnconfigure(1, weight=1)
        self.simulationFrame.columnconfigure(2, weight=1)

        # Labels
        self.sl1 = Label(self.simulationFrame, text='Simulation Settings', justify="center", font=self.font_header)
        self.sl1.grid(row=0, column=0, columnspan=3, sticky=N+E+S+W)
        self.sl2 = Label(self.simulationFrame, text='Market Type*:', justify="center", font=self.font)
        self.sl2.grid(row=1, column=0, sticky=N+E+S+W)
        self.sl3 = Label(self.simulationFrame, text='Crypto (Default: 1000):', justify="center", font=self.font)
        self.sl3.grid(row=2, column=0, sticky=N+E+S+W)
        self.sl4 = Label(self.simulationFrame, text='Fiat (Default: 100):', justify="center", font=self.font)
        self.sl4.grid(row=3, column=0, sticky=N+E+S+W)
        self.sl5 = Label(self.simulationFrame, text='File Path*:', justify="center", font=self.font)
        self.sl5.grid(row=4, column=0, sticky=N+E+S+W)

        # Entries
        self.se1 = Entry(self.simulationFrame, font=self.font)
        self.se1.grid(row=2, column=1, sticky=N+E+S+W)
        self.se2 = Entry(self.simulationFrame, font=self.font)
        self.se2.grid(row=3, column=1, sticky=N+E+S+W)
        self.se3 = Entry(self.simulationFrame, font=self.font)
        self.se3.insert(0, 'data/ohlcv_data.json')
        self.se3.grid(row=4, column=1, sticky=N+E+S+W)

        # Dropdowns
        self.menu3 = StringVar()
        self.menu3.set("Select a market type")
        self.sd1 = OptionMenu(self.simulationFrame, self.menu3, *self.market_strategies)
        self.sd1.config(font=self.font)
        menu = self.simulationFrame.nametowidget(self.sd1.menuname)
        menu.config(font=self.font)
        self.sd1.grid(row=1, column=1, sticky=N+E+S+W)

        # Checkboxes
        self.var1 = IntVar()
        self.sc1 = Checkbutton(self.simulationFrame, text='CSV', variable=self.var1, onvalue=1, offvalue=0,
                               font=self.font)
        self.sc1.grid(row=4, column=2, sticky=N+E+S+W)

        # Buttons
        self.b1 = Button(self.simulationFrame, text='Run Simulation', command=self.simulation_callback,
                         state='disabled', font=self.font)
        self.b1.grid(row=5, column=0, columnspan=3, sticky=N+E+S+W)

        ################################################################################################################
        # Live Frame
        self.liveFrame = Frame(self.bottomFrame, borderwidth=2, relief=SUNKEN)
        self.liveFrame.grid(row=0, column=3, sticky=N+E+S+W, padx=5, pady=5)
        self.liveFrame.rowconfigure(1, weight=1)
        self.liveFrame.columnconfigure(0, weight=1)
        self.liveFrame.columnconfigure(1, weight=1)

        # Labels
        self.ll1 = Label(self.liveFrame, text='Live Buttons', justify="center", font=self.font_header)
        self.ll1.grid(row=0, column=0, columnspan=2, sticky=N+E+S+W)

        # Buttons
        self.b2 = Button(self.liveFrame, text='Start Live', command=self.start_live_callback, state='disabled',
                         font=self.font)
        self.b2.grid(row=1, column=0, sticky=N+E+S+W)
        self.b3 = Button(self.liveFrame, text='Stop Live', command=self.stop_live_callback, state='disabled',
                         font=self.font)
        self.b3.grid(row=1, column=1, sticky=N+E+S+W)

        ################################################################################################################
        # Plot Frame
        self.plotFrame = Frame(self.topFrame, borderwidth=2, relief=SUNKEN)
        self.plotFrame.pack(fill='both', expand=True)

        # Matplotlib Figure
        self.fig = mpf.figure(figsize=(12, 8), dpi=100)

        # Load data
        data = self.fl.load_plot_data('data/ohlcv_data.json')

        # Reformat data
        reformatted_data = dict()
        reformatted_data['Date'] = []
        reformatted_data['Open'] = []
        reformatted_data['High'] = []
        reformatted_data['Low'] = []
        reformatted_data['Close'] = []
        reformatted_data['Volume'] = []
        for d in data:
            reformatted_data['Date'].append(datetime.fromtimestamp(d[0] / 1000))
            reformatted_data['Open'].append(d[1])
            reformatted_data['High'].append(d[2])
            reformatted_data['Low'].append(d[3])
            reformatted_data['Close'].append(d[4])
            reformatted_data['Volume'].append(d[5])
        pdata = pd.DataFrame.from_dict(reformatted_data)
        pdata.set_index('Date', inplace=True)

        # Create plots and plot data
        self.plot1 = self.fig.add_subplot(211)
        self.plot2 = self.fig.add_subplot(212, sharex=self.plot1)
        mpf.plot(pdata, axtitle=self.title, type=self.type, ax=self.plot1, volume=self.plot2, style=self.style)
        # self.fig.tight_layout()
        self.fig.subplots_adjust(hspace=.0)

        # Creating the Tkinter canvas containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.plotFrame, pack_toolbar=False)
        toolbar.update()
        toolbar.pack()  # fill='both', expand=True

    ####################################################################################################################
    # General Callbacks
    def exit_callback(self):
        plt.close('all')
        self.master.destroy()

    ####################################################################################################################
    # NDAX Menu Callbacks
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
    # Plot Menu Callback
    def style_callback(self, s):
        self.style = s

        # Load data
        data = self.fl.load_plot_data('data/ohlcv_data.json')

        # Reformat data
        reformatted_data = dict()
        reformatted_data['Date'] = []
        reformatted_data['Open'] = []
        reformatted_data['High'] = []
        reformatted_data['Low'] = []
        reformatted_data['Close'] = []
        reformatted_data['Volume'] = []
        for d in data:
            reformatted_data['Date'].append(datetime.fromtimestamp(d[0] / 1000))
            reformatted_data['Open'].append(d[1])
            reformatted_data['High'].append(d[2])
            reformatted_data['Low'].append(d[3])
            reformatted_data['Close'].append(d[4])
            reformatted_data['Volume'].append(d[5])
        pdata = pd.DataFrame.from_dict(reformatted_data)
        pdata.set_index('Date', inplace=True)

        # Clear the plots and plot new data
        self.plot1.cla()
        self.plot2.cla()
        mpf.plot(pdata, axtitle=self.title, type=self.type, ax=self.plot1, volume=self.plot2, style=self.style)
        self.canvas.draw()

    def type_callback(self, t):
        self.type = t

        # Load data
        data = self.fl.load_plot_data('data/ohlcv_data.json')

        # Reformat data
        reformatted_data = dict()
        reformatted_data['Date'] = []
        reformatted_data['Open'] = []
        reformatted_data['High'] = []
        reformatted_data['Low'] = []
        reformatted_data['Close'] = []
        reformatted_data['Volume'] = []
        for d in data:
            reformatted_data['Date'].append(datetime.fromtimestamp(d[0] / 1000))
            reformatted_data['Open'].append(d[1])
            reformatted_data['High'].append(d[2])
            reformatted_data['Low'].append(d[3])
            reformatted_data['Close'].append(d[4])
            reformatted_data['Volume'].append(d[5])
        pdata = pd.DataFrame.from_dict(reformatted_data)
        pdata.set_index('Date', inplace=True)

        # Clear the plots and plot new data
        self.plot1.cla()
        self.plot2.cla()
        mpf.plot(pdata, axtitle=self.title, type=self.type, ax=self.plot1, volume=self.plot2, style=self.style)
        self.canvas.draw()

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

        # Load data
        data = self.fl.load_plot_data('data/ohlcv_data.json')

        # Reformat data
        reformatted_data = dict()
        reformatted_data['Date'] = []
        reformatted_data['Open'] = []
        reformatted_data['High'] = []
        reformatted_data['Low'] = []
        reformatted_data['Close'] = []
        reformatted_data['Volume'] = []
        for d in data:
            reformatted_data['Date'].append(datetime.fromtimestamp(d[0] / 1000))
            reformatted_data['Open'].append(d[1])
            reformatted_data['High'].append(d[2])
            reformatted_data['Low'].append(d[3])
            reformatted_data['Close'].append(d[4])
            reformatted_data['Volume'].append(d[5])
        pdata = pd.DataFrame.from_dict(reformatted_data)
        pdata.set_index('Date', inplace=True)

        # Clear the plots and plot new data
        self.plot1.cla()
        self.plot2.cla()
        self.title = tf + ' ' + pair + ' Graph (' + str(limit) + ' data points)'
        mpf.plot(pdata, axtitle=self.title, type=self.type, ax=self.plot1, volume=self.plot2, style=self.style)
        self.canvas.draw()

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
        self.b2['state'] = 'normal'

    def create_grid(self, intervals, min_val, max_val, amount_per_int, tolerance):
        # Sample inputs: intervals=18, min_val=0.155, max_val=0.177, amount_per_int=100, tolerance=4
        self.grid = GridTrade(intervals, min_val, max_val, amount_per_int, tolerance, self.ndax)
        states = self.grid.get_states()
        for s in states.values():
            self.plot1.axhline(y=s, color='b', linestyle='--', linewidth=0.5)

    ####################################################################################################################
    # Simulation Button Callbacks
    def simulation_callback(self):
        file_path = self.se3.get()
        if self.var1 == 1:
            self.run_paper_simulation(file_path, True)
        else:
            self.run_paper_simulation(file_path)

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
            s.live_trade('DOGE', 'DOGE/CAD', 'ask')
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

    ####################################################################################################################
    # Live Button Callbacks
    def start_live_callback(self):
        self.b2['state'] = 'disabled'
        self.b3['state'] = 'normal'
        print('Live Trading Started...')
        # If we don't already have a running thread, start a new one
        if not self.live_thread:
            s = Strategy(self.grid, self.ndax)
            fig = plt.figure()
            plt.show()
            self.live_thread = LiveThread(s, fig)
            self.live_thread.start()

    def stop_live_callback(self):
        self.b2['state'] = 'normal'
        self.b3['state'] = 'disabled'
        print('Live Trading Ended.')
        # If we have one running, stop it
        if self.live_thread:
            self.live_thread.stop()
            self.live_thread = None
