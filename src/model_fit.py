import pandas as pd
import numpy as np
import fbprophet
from fbprophet import Prophet


class prophet_model:
    def __init__(self, data, feature, label):
        self.data = data
        self.feature = feature
        self.label = label
        self.df = self.data_prepare()
    def data_prepare(self):
        if self.data is None:
            pass
        elif len(self.feature) >= 1:
            if self.label:
                self.data['y']=self.data[self.label].shift(periods=-1)
                df = self.data.reset_index()
                df = df.dropna()
                df.rename(columns={'Date': 'ds'}, inplace=True)
                select_col = ['ds'] + self.feature + ['y']
                df = df[select_col]
                return df
            else:
                df = self.data.reset_index()
                df.rename(columns={'Date': 'ds'}, inplace=True)
                select_col = ['ds'] + self.feature
                df = df[select_col]
                return df    
        elif len(self.feature) < 1 and self.label:
            df = self.data[self.label].reset_index()
            df.columns = ['ds', 'y']
            return df
    def model_fit(self):
        if len(self.feature) > 1:
            m = Prophet()
            for f in self.feature:
                m.add_regressor(f)
            m.fit(self.df)
            return m
        else:
            m = Prophet()
            m.fit(self.df)
            return m
    def model_predict(self, model, window=None):
        if len(self.feature) >= 1:
            if self.label:
                y_true = self.df['y']
                df_pred = self.df.drop(columns=['y'])
                forecast = model.predict(df_pred)
                forecast['y_true'] = y_true
                return forecast
            else:
                forecast = model.predict(self.df)
                return forecast
        elif window is not None:
            future = model.make_future_dataframe(periods=window)
            forecast = model.predict(future)
            if self.label and self.data:
                f = self.df.merge(forecast, how='left', left_on='ds', right_on='ds')
                y_true = self.df['y']
                f['y_true'] = y_true
                return f
            else:
                f = forecast.tail(window+1)
                return f