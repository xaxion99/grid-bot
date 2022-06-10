import ccxt
import os
from dotenv import load_dotenv
from gui import GUI
from test import Test
from tkinter import Tk


def main(login):
    root = Tk()
    app = GUI(root, login)
    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Load in environment variables from .env file
    load_dotenv()
    APIKEY = os.getenv('APIKEY')
    SECRET = os.getenv('SECRET')
    UID = os.getenv('UID')
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')

    # Create NDAX API access header
    ndax = ccxt.ndax({
        'apiKey': APIKEY,
        'secret': SECRET,
        'uid': UID,
        'login': LOGIN,
        'password': PASSWORD
    })
    print('Successfully loaded in environment variables.')

    # Test code
    test = Test(ndax)
    # test.test()
    # test.load_ticker_data()
    print('Testing is complete.')

    # Start GUI
    main(ndax)
