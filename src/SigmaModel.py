import os
from datetime import datetime
import datetime as dt
from src.data_extract import yahoo
from src.model import MLProphet

import pandas as pd


class SigmaModel:
    FEATURES = 'Open,High,Low,Close,Adj Close,Volume'.split(",")
    LABEL = os.environ.get("LABEL", "Open")

    def __init__(self, ticker, current_date):
        train_start = (datetime.strptime(current_date, "%Y-%m-%d").date() - dt.timedelta(365)).strftime("%Y-%m-%d")
        train_end = current_date

        self.current_date = current_date
        self.ticker = ticker

        yh_train = yahoo(ticker, train_start, train_end)
        data_yh_train = yh_train.collect_data()

        self.model = MLProphet(data_yh_train, self.FEATURES, self.LABEL)
        self.model.model_fit()

        self.high_model = MLProphet(data_yh_train, self.FEATURES, 'High')
        self.high_model.model_fit()

        self.low_model = MLProphet(data_yh_train, self.FEATURES, "Low")
        self.low_model.model_fit()

        self.close_model = MLProphet(data_yh_train, self.FEATURES, "Close")
        self.close_model.model_fit()

        self.adj_close_model = MLProphet(data_yh_train, self.FEATURES, "Adj Close")
        self.adj_close_model.model_fit()

        self.volume_model = MLProphet(data_yh_train, self.FEATURES, "Volume")
        self.volume_model.model_fit()

    def __get_predict_data(self):
        pred_start = (datetime.strptime(self.current_date, "%Y-%m-%d").date() - dt.timedelta(1)).strftime("%Y-%m-%d")
        # (current_date-1, current_date)
        yh_pred = yahoo(self.ticker, pred_start, self.current_date)
        return yh_pred.collect_data()

    def model_predict(self, future_data):
        forecast = self.model.model_predict(future_data)
        # print("open model \n")
        # print("For " + date + " forecast is \n")
        # print(forecast)
        # print(future_data)
        # print("\n")
        return forecast

    def predict(self, window):

        # print(" Predicted price for " + self.ticker + " starting from " + self.current_date + " for " + str(window) + " day is \n")

        predictions = pd.DataFrame()
        data_yh_pred = self.__get_predict_data()

        current_date = self.current_date
        forecast = self.model_predict(data_yh_pred)
        predictions[current_date] = forecast.iloc[[0]][['yhat']]
        while window > 1:
            future = pd.DataFrame()
            future['Open'] = forecast.iloc[[0]]['yhat']
            forecast = self.high_model.model_predict(data=data_yh_pred)
            future['High'] = forecast.reset_index().iloc[[0]]['yhat']
            # print(forecast)
            forecast = self.low_model.model_predict(data=data_yh_pred)
            future['Low'] = forecast.reset_index().iloc[[0]]['yhat']
            # print(forecast)
            forecast = self.close_model.model_predict(data=data_yh_pred)
            future['Close'] = forecast.reset_index().iloc[[0]]['yhat']
            # print(forecast)
            forecast = self.adj_close_model.model_predict(data=data_yh_pred)
            future['Adj Close'] = forecast.reset_index().iloc[[0]]['yhat']
            # print(forecast)
            forecast = self.volume_model.model_predict(data=data_yh_pred)
            future['Volume'] = forecast.reset_index().iloc[[0]]['yhat']
            # print(forecast)
            future['Date'] = current_date
            future.set_index("Date")
            next_date = (datetime.strptime(current_date, "%Y-%m-%d").date() + dt.timedelta(1)).strftime("%Y-%m-%d")
            forecast = self.model_predict(future)
            window = window-1
            current_date = next_date
            data_yh_pred = future
            predictions[current_date] = forecast.iloc[[0]][['yhat']]

        predictions.reset_index()
        return predictions.to_dict()

