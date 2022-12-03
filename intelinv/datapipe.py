import ssl
import datetime
import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info as si


## indicator configs
_BASIC_COLS = ['index', 'marketCap', 'sector', 'industry']
_STOCK_COLS = ['currentPrice', 'averageVolume', 'trailingPE', 'trailingEps', 'priceToBook', '52WeekChange', 'fiftyTwoWeekHigh','fiftyTwoWeekLow','fiftyDayAverage']
_MARKET_COLS = ['shortRatio']
_FINANCIAL_COLS = ['ebitdaMargins', 'profitMargins', 'freeCashflow', 'returnOnAssets', 'returnOnEquity','debtToEquity']
_GROWTH_COLS = ['revenueGrowth', 'earningsGrowth', 'earningsQuarterlyGrowth', 'payoutRatio']
_TCA = 'Total Current Assets'
_TL = 'Total Liab'
_TE = 'Total Stockholder Equity'
_MC = 'marketCap'
_NWC = 'Net Working Capital'
_SEL_COL = _BASIC_COLS+_STOCK_COLS+_MARKET_COLS+_FINANCIAL_COLS+_GROWTH_COLS+[_TCA, _TL, _TE]
_SYMBOL = 'Symbol'


## file configs
filename = 'daily_stock_data.csv'
htmllink = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


class datadownloader():
    def __init__(self, sel_col, filename, htmllink):
        self.sel_col = sel_col
        self.filename = filename
        self.htmllink = htmllink
        self.ticker_list = None

    def _get_sp_ticker_list(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        table=pd.read_html(self.htmllink)
        ticker_list = table[0]
        return ticker_list[_SYMBOL]

    def _download_stock_data(self):
        self.ticker_list = self._get_sp_ticker_list()
        ticker_list_str = " ".join(self.ticker_list)
        print(f"Pulling info for below tickers: {ticker_list_str}")
        data = yf.Tickers(ticker_list_str)
        print("Pulled ticker info from Yahoo Finance API!")
        info_dict = {}
        cnt = 0
        cnt_tot = len(self.ticker_list)
        t_start = datetime.datetime.now()
        t_last = t_start
        t_accum = datetime.timedelta()
        for ticker in self.ticker_list:
            t = data.tickers[ticker]
            info = t.info
            if _TCA in t.quarterly_balance_sheet.index:
                info[_TCA] = t.quarterly_balance_sheet[t.quarterly_balance_sheet.index==_TCA].values[0][0]
            else:
                info[_TCA] = 0
            if _TL in t.quarterly_balance_sheet.index:
                info[_TL] = t.quarterly_balance_sheet[t.quarterly_balance_sheet.index==_TL].values[0][0]
            else:
                info[_TL] = 0
            if _TE in t.quarterly_balance_sheet.index:
                info[_TE] = t.quarterly_balance_sheet[t.quarterly_balance_sheet.index==_TE].values[0][0]
            else:
                info[_TE] = 0           
            info_dict.update({ticker: t.info})
            cnt += 1
            t_curr = datetime.datetime.now() - t_last
            t_last = datetime.datetime.now()
            t_accum += t_curr
            print(f"Finished processing {ticker}! \t {cnt} / {cnt_tot} - time used: {t_curr}, avg time used: {t_accum / cnt}, estimate remaining time: {t_accum / cnt * (cnt_tot - cnt)}")
        
        df = pd.DataFrame(info_dict).T.reset_index()
        df_sel = df[_SEL_COL]
        df_sel[_NWC] = df_sel[_TCA] - df_sel[_TL]
        df_sel.to_csv(filename)
        print("Downloaded stock data!")
        

def main():
    dd = datadownloader(_SEL_COL, filename, htmllink)
    dd._download_stock_data()
    
    
if __name__ == '__main__':
    main()