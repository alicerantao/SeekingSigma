import numpy as np
import pandas as pd
import datetime as dt
from pytrends.request import TrendReq


def load_data(key_word):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=['{}'.format(key_word)])
    data = pytrend.interest_over_time()
    data = data.reset_index()

    return data[['date', '{}'.format(kw)]]
