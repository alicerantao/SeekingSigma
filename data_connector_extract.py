from abc import ABC, abstractmethod
from pytrends.request import TrendReq
import yfinance as yf
import pandas as pd
import datetime as dt
from datetime import timedelta, date
from datetime import datetime


class extract(ABC):
    def __init__(self, start:str, end:str) -> None:
        self.start = start
        self.end = end
    def connect_API(self) -> None: pass
    @abstractmethod
    def collect_data(self): pass


class gtrend(extract):
    def __init__(self, keyword:str, start:str, end:str) -> None:
        self.keyword = keyword
        super().__init__(start, end)
        self.connect_API()
        
    def connect_API(self):
        self.pytrend = TrendReq()

    def collect_data(self):
        self.pytrend.build_payload(kw_list=['{}'.format(self.keyword)])
        data = self.pytrend.interest_over_time().reset_index()
        df = data[['date', '{}'.format(self.keyword)]]
        df_trend = df.loc[df.index.repeat(7)]
        df_trend['date'] = pd.to_datetime(df_trend['date'])
        min_date = df_trend['date'].min()
        max_date = df_trend['date'].max()+timedelta(days=6)
        df_trend['GT_date'] = pd.date_range(start=min_date, end=max_date).tolist()
        sd = datetime.strptime(self.start, "%Y-%m-%d").date()
        ed = datetime.strptime(self.end, "%Y-%m-%d").date()
        df_trend = df_trend[(df_trend['GT_date'].dt.date>=sd)&(df_trend['GT_date'].dt.date<=ed)]
        data_trend = df_trend[['GT_date', '{}'.format(keyword)]]
        return data_trend

class yahoo(extract):
    def __init__(self, keyword:str, start:str, end:str) -> None:
        self.ticker = ticker
        super().__init__(start, end)

    def collect_data(self):
        data = yf.download(self.ticker, start=self.start, end=self.end)
        return data