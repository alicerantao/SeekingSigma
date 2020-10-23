import numpy as np
import pandas as pd
import datetime as dt
from pytrends.request import TrendReq
from datetime import timedelta, date
import datetime

def load_data(key_word, start_date, end_date):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=['{}'.format(key_word)])
    data = pytrend.interest_over_time()
    data = data.reset_index()
    df = data[['date', '{}'.format(key_word)]]

    ## repeat 7 times per row
    df_trend = df.loc[df.index.repeat(7)]
    ## format date
    df_trend['date']=pd.to_datetime(df_trend['date'])
    ## create list of date range
    min_date=df_trend['date'].min()
    max_date= df_trend['date'].max()+timedelta(days=6)
    datelist = pd.date_range(start=min_date, end=max_date).tolist()
    ## assign formated date to df_trend
    df_trend['GT_date']=datelist
    ## filter by start_date and end date
    sd=date.fromisoformat(start_date)
    ed=date.fromisoformat(end_date)
    trend_df = df_trend[(df_trend['GT_date'].dt.date>=sd)&(df_trend['GT_date'].dt.date<=ed)]
    data_trend = trend_df[['GT_date', '{}'.format(key_word)]]

    return data_trend

