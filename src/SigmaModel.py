import datetime as dt
import os
from datetime import datetime

import pandas as pd

from src.data_extract import yahoo
from src.model import MLProphet


class SigmaModel:
    FEATURES = "Open,High,Low,Close,Adj Close,Volume".split(",")
    LABEL = os.environ.get("LABEL", "Open")

    def __init__(self, ticker, current_date):
        train_start = (
            datetime.strptime(current_date, "%Y-%m-%d").date() - dt.timedelta(365)
        ).strftime("%Y-%m-%d")
        train_end = current_date

        self.current_date = current_date
        self.ticker = ticker

        yh_train = yahoo(ticker, train_start, train_end)
        data_yh_train = yh_train.collect_data()

        self.model = MLProphet(data_yh_train, self.FEATURES, self.LABEL)
        self.model.model_fit()

        self.high_model = MLProphet(data_yh_train, self.FEATURES, "High")
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
        pred_start = (
            datetime.strptime(self.current_date, "%Y-%m-%d").date() - dt.timedelta(1)
        ).strftime("%Y-%m-%d")
        # (current_date-1, current_date)
        yh_pred = yahoo(self.ticker, pred_start, self.current_date)
        return yh_pred.collect_data()

    def predict(self, window):
        predictions = pd.DataFrame()
        data_yh_pred = self.__get_predict_data()

        current_date = self.current_date
        forecast = self.model.model_predict(data_yh_pred)
        predictions[current_date] = forecast.iloc[[0]][["yhat"]]
        while window > 1:
            future = pd.DataFrame()
            future["Open"] = forecast.iloc[[0]]["yhat"]
            high_forecast = self.high_model.model_predict(data=data_yh_pred)
            future["High"] = high_forecast.reset_index().iloc[[0]]["yhat"]
            # print(forecast)
            low_forecast = self.low_model.model_predict(data=data_yh_pred)
            future["Low"] = low_forecast.reset_index().iloc[[0]]["yhat"]
            # print(forecast)
            close_forecast = self.close_model.model_predict(data=data_yh_pred)
            future["Close"] = close_forecast.reset_index().iloc[[0]]["yhat"]
            # print(forecast)
            adj_close_forecast = self.adj_close_model.model_predict(data=data_yh_pred)
            future["Adj Close"] = adj_close_forecast.reset_index().iloc[[0]]["yhat"]
            # print(forecast)
            volume_forecast = self.volume_model.model_predict(data=data_yh_pred)
            future["Volume"] = volume_forecast.reset_index().iloc[[0]]["yhat"]
            # print(forecast)
            future["Date"] = current_date
            future.set_index("Date")
            next_date = (
                datetime.strptime(current_date, "%Y-%m-%d").date() + dt.timedelta(1)
            ).strftime("%Y-%m-%d")
            forecast = self.model.model_predict(future)
            window = window - 1
            current_date = next_date
            data_yh_pred = future
            predictions[current_date] = forecast.iloc[[0]][["yhat"]]

        predictions.reset_index()
        return predictions.to_dict()
