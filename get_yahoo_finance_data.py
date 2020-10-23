import argparse
from pandas_datareader import data as pdr
from datetime import date
import yfinance as yf
import pandas as pd


def getData(ticker, start_date, end_date):
    print (ticker)
    data = yf.download(ticker, start=start_date, end=end_date)
    dataname= ticker+'_'+str(today)
    saveData(data, dataname )
    return dataname + '.csv'

# Create a data folder in your current dir.
def saveData(df, filename):
    df.to_csv('./' + filename + '.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--tickers',
        help='List of tickers separted by ,',
        dest='ticker_list',
        required=True,
        default=[],
        nargs='+',
    )
    parser.add_argument(
        '--start_date',
        help='Start date str in this format yyyy-mm-dd',
        dest='start_date',
        required=True,
        default='',
    )
    parser.add_argument(
        '--end_date',
        help='End date str in this format yyyy-mm-dd',
        dest='end_date',
        required=True,
        default='',
    )
    args = parser.parse_args()

    today = date.today()

    files = []
    for tik in args.ticker_list:
        files.append(getData(tik, args.start_date, args.end_date))

    print(files)
