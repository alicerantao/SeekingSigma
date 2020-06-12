import numpy as np
import pandas as pd
import argparse
from fbprophet import Prophet
import datetime as dt
from sklearn.metrics import r2_score
from pytrends.request import TrendReq


def parse_argument():
    parser=argparse.ArgumentParser(description='import parameters')
    parser.add_argument('--key_word', help='key word of interest', required=True)
    parser.add_argument('--training_cap', help='training data market cap', required=True)
    parser.add_argument('--training_range', help='number of training date', required=True)
    parser.add_argument('--growth', help='data growth type', required=True)
    parser.add_argument('--changepoints', help='data change points', required=False)
    parser.add_argument('--holidays', help='holiday period', required=False)
    parser.add_argument('--yearly_seasonality', help='data yearly seasonality', required=False)
    parser.add_argument('--pred_cap', help='training data market cap', required=True)
    parser.add_argument('--period', help='prediction period', required=True)


def load_data(key_word):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=['{}'.format(key_word)])
    data = pytrend.interest_over_time()
    data = data.reset_index()

    return data[['date', '{}'.format(kw)]]


def process_data(data, training_cap, training_range):
    data['date'] = pd.to_datetime(data['date'])
    data['cap'] = training_cap
    data.columns = ['ds', 'y', 'cap']
    data = data.iloc[-training_range:-1, :]

    return data


def model_training(data, growth, changepoints=None, holidays=None, yearly_seasonality=True):
    model = Prophet(growth=growth, changepoints=changepoints, holidays=holidays, yearly_seasonality=yearly_seasonality)
    model.fit(data)

    return model


def model_predict(model, data, pred_cap, period):
    future = model.make_future_dataframe(periods=period)
    future['cap'] = pred_cap
    forecast = model.predict(future)
    n=data.shape[0]
    data_training_pred = forecast.loc[:n-1, ['yhat', 'yhat_lower', 'yhat_upper']]
    data_scoring_pred = forecast.loc[n:, ['yhat', 'yhat_lower', 'yhat_upper']]

    Train_Rsquare=r2_score(data.iloc[:, 1], data_training_pred['yhat'])
    print('Train Rsquare: {:0.2f}'.format(Train_Rsquare))
    print(data_scoring_pred)

    return data_scoring_pred


def main():
    args = parse_argument()
    df = load_data(**vars(args))
    data = process_data(df, **vars(args))
    model = model_training(data, **vars(args))
    data_scoring_pred = model_predict(model, data, **vars(args))
    
