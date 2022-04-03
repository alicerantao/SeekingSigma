import os
from src.model import MLProphet
from src.data_extract import yahoo
from sklearn.metrics import r2_score
from datetime import datetime
import datetime as dt


TICKER = os.environ.get("TICKER", "tsla")
LABEL = os.environ.get("LABEL", "Open")
# CURRENT_DATE = os.environ.get("CURRENT_DATE", datetime.today().strftime("%Y-%m-%d"))
CURRENT_DATE = "2022-04-01"
WINDOW = os.environ.get("WINDOW", 1)

FEATURES = 'Open,High,Low,Close,Adj Close,Volume'.split(",")


if __name__ == '__main__':
    # TODO: Adjust dates based on weekdays.
    start_date = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() - dt.timedelta(365)).strftime("%Y-%m-%d")

    train_start = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() - dt.timedelta(365)).strftime("%Y-%m-%d")
    train_end = CURRENT_DATE
    pred_start = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() - dt.timedelta(1)).strftime("%Y-%m-%d")
    pred_end = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() + dt.timedelta(WINDOW-1)).strftime("%Y-%m-%d")

    yh_train = yahoo(TICKER, train_start, train_end)
    data_yh_train = yh_train.collect_data()

    yh_pred = yahoo(TICKER, pred_start, pred_end)
    data_yh_pred = yh_pred.collect_data()

    print(data_yh_pred)

    model = MLProphet(data_yh_train, FEATURES, LABEL)
    model.model_fit()

    # open_model = MLProphet(data_yh_train, [], 'Open')
    # open_model.model_fit()
    #
    # high_model = MLProphet(data_yh_train, [], 'High')
    # high_model.model_fit()
    #
    # low_model = MLProphet(data_yh_train, [], "Low")
    # low_model.model_fit()
    #
    # close_model = MLProphet(data_yh_train, [], "Close")
    # close_model.model_fit()
    #
    # adj_close_model = MLProphet(data_yh_train, [], "Adj Close")
    # adj_close_model.model_fit()
    #
    # volume_model = MLProphet(data_yh_train, [], "Volume")
    # volume_model.model_fit()

    forecast = model.model_predict(data_yh_pred)
    print(" Predicted price for " + TICKER + " starting from " + pred_start + " for " + str(WINDOW) + " day is \n")
    # print(forecast)
    print("open model \n")
    print(forecast)
    print(data_yh_pred)
    print("\n")
    # print(f"r2 score is {r2_score(forecast.y_true, forecast.yhat)}")


