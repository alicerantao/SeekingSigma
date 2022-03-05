import os
from src.model import MLProphet
from src.data_extract import yahoo
from sklearn.metrics import r2_score
from datetime import datetime
import datetime as dt


TICKER = os.environ.get("TICKER", "msft")
FEATURES = os.environ.get("FEATURES", 'High,Low,Close,Adj Close,Volume').split(",")
LABEL = os.environ.get("LABEL", "Open")
CURRENT_DATE = os.environ.get("CURRENT_DATE", datetime.today().strftime("%Y-%m-%d"))
WINDOW = os.environ.get("WINDOW", 1)


if __name__ == '__main__':
    start_date = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() - dt.timedelta(365)).strftime("%Y-%m-%d")

    train_start = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() - dt.timedelta(365)).strftime("%Y-%m-%d")
    train_end = CURRENT_DATE
    pred_start = train_end
    pred_end = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() + dt.timedelta(WINDOW+5)).strftime("%Y-%m-%d")

    yh_train = yahoo(TICKER, train_start, train_end)
    data_yh_train = yh_train.collect_data()

    yh_pred = yahoo(TICKER, pred_start, pred_end)
    data_yh_pred = yh_pred.collect_data()

    train = MLProphet(data_yh_train, FEATURES, LABEL)
    train.model_fit()

    forecast = train.model_predict(data_yh_pred, window=WINDOW)
    print(" Predicted price for " + TICKER + " starting from " + pred_start + " for " + str(WINDOW) + " day is \n")
    print(forecast)
    print(r2_score(forecast.y_true, forecast.yhat))
