from prophet import Prophet


class MLProphet:
    def __init__(self, data, features, label):
        self.features = features
        self.label = label
        self.df = self.data_prepare(data)
        self.model = None

    def data_prepare(self, data, predict=False):
        """
        Prepare data in the prophet model training format.

        Args:
            data: (pd.DataFrame) Training dataset or testing dataset.

        Returns:
            The processed dataframe.
        """
        if data is None:
            pass
        elif len(self.features) >= 1:
            # TODO: Check if data has the label.
            if self.label:
                data['y']=data[self.label].shift(periods=-1)
                df = data.reset_index()
                df = df.dropna() if not predict else df
                df.rename(columns={'Date': 'ds'}, inplace=True)
                select_col = ['ds'] + self.features + ['y']
                df = df[select_col]
                return df
            else:
                df = data.reset_index()
                df.rename(columns={'Date': 'ds'}, inplace=True)
                select_col = ['ds'] + self.features
                df = df[select_col]
                return df    
        elif len(self.features) < 1 and self.label:
            data['y'] = data[self.label].shift(periods=-1)
            df = data[self.label].reset_index()
            df = df.dropna() if not predict else df
            df.rename(columns={'Date': 'ds'}, inplace=True)
            df.columns = ['ds', 'y']
            return df

    def model_fit(self) -> None:
        """
        Train prophet model with processed data.
        """
        self.model = Prophet()
        if len(self.features) > 1:
            for f in self.features:
                self.model.add_regressor(f)
        self.model.fit(self.df)
        return

    def model_predict(self, data=None,  window=None):
        """
        Generate prediction using the passed estimator

        Args:
            data: (object) The test data.
            window: (int) The number of days for prediction.
        
        Returns:
            The dataframe with forecast.
        """
        df = self.data_prepare(data, True)
        if len(self.features) >= 1:
            if self.label:
                y_true = df['y']
                df_pred = df.drop(columns=['y'])
                forecast = self.model.predict(df_pred)
                forecast['y_true'] = y_true
                return forecast
            else:
                forecast = self.model.predict(df)
                return forecast
        elif window is not None:
            future = self.model.make_future_dataframe(periods=window)
            forecast = self.model.predict(future)
            if self.label and data:
                f = df.merge(forecast, how='left', left_on='ds', right_on='ds')
                y_true = df['y']
                f['y_true'] = y_true
                return f
            else:
                f = forecast.tail(window+1)
                return f
