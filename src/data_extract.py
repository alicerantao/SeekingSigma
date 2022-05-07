import datetime as dt
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta

import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq


class extract(ABC):
    """Interface for data extraction.

    The class serves as an Interface of data extraction for
    different data sources.

    Attributes:
        start: The start date of the extracted data.
        end: The end date of the extracted data.
    """

    def __init__(self, start: str, end: str) -> None:
        """Inits base class with start and end date"""
        self.start = start
        self.end = end

    def connect_API(self) -> None:
        pass

    @abstractmethod
    def collect_data(self):
        pass


class gtrend(extract):
    """Google trend data extraction.

    The class connects to Google trend API for data download
    and returns the processed data in DataFrame.

    Attributes:
        keyword: (str) The word of interest for trend data download.
        start: (str) The start date of extracted data.
        end: (str) The end date of extracted data.
    """

    def __init__(self, keyword: str, start: str, end: str) -> None:
        self.keyword = keyword
        super().__init__(start, end)
        self.connect_API()

    def connect_API(self):
        """Connect to Google trend API"""
        self.pytrend = TrendReq()

    def collect_data(self):
        """Download data and process data.

        Args:
            keyword: (str) The word of interest for trend data download.
            start: (str) The start date of extracted data.
            end: (str) The end date of extracted data.

        Returns:
            The processed dataframe.
        """
        self.pytrend.build_payload(kw_list=["{}".format(self.keyword)])
        data = self.pytrend.interest_over_time().reset_index()
        df = data[["date", "{}".format(self.keyword)]]
        df_trend = df.loc[df.index.repeat(7)]
        df_trend["date"] = pd.to_datetime(df_trend["date"])
        min_date = df_trend["date"].min()
        max_date = df_trend["date"].max() + timedelta(days=6)
        df_trend["GT_date"] = pd.date_range(start=min_date, end=max_date).tolist()
        sd = datetime.strptime(self.start, "%Y-%m-%d").date()
        ed = datetime.strptime(self.end, "%Y-%m-%d").date()
        df_trend = df_trend[
            (df_trend["GT_date"].dt.date >= sd) & (df_trend["GT_date"].dt.date <= ed)
        ]
        data_trend = df_trend[["GT_date", "{}".format(keyword)]]
        return data_trend


class yahoo(extract):
    """Yahoo finance data extraction.

    The class connects to Yahoo Finance for data download
    and returns the processed data in DataFrame.

    Attributes:
        ticker: (str) The ticker of stock for data download.
        start: (str) The start date of extracted data.
        end: (str) The end date of extracted data.
    """

    def __init__(self, ticker: str, start: str, end: str) -> None:
        self.ticker = ticker
        super().__init__(start, end)

    def collect_data(self):
        """Download data and process data

        Args:
            ticker: (str) The ticker of stock for data download.
            start: (str) The start date of extracted data.
            end: (str) The end date of extracted data.

        Returns:
            The processed dataframe.
        """
        data = yf.download(self.ticker, start=self.start, end=self.end)
        return data
