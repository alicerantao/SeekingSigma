from flask import Flask
from flask_restful import Resource, Api, reqparse
from src.model import MLProphet
from src.data_extract import yahoo
from sklearn.metrics import r2_score
from datetime import datetime
import datetime as dt
import os


app = Flask(__name__)
api = Api(app)

FEATURES = os.environ.get("FEATURES", 'High,Low,Close,Adj Close,Volume').split(",")
LABEL = os.environ.get("LABEL", "Open")

def train_pred(CURRENT_DATE, TICKER, WINDOW, FEATURES, LABEL):
    start_date = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() - dt.timedelta(365)).strftime("%Y-%m-%d")
    train_start = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() - dt.timedelta(365)).strftime("%Y-%m-%d")
    train_end = CURRENT_DATE
    pred_start = train_end
    pred_end = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() + dt.timedelta(WINDOW+1)).strftime("%Y-%m-%d")

    yh_train = yahoo(TICKER, train_start, train_end)
    data_yh_train = yh_train.collect_data()

    yh_pred = yahoo(TICKER, pred_start, pred_end)
    data_yh_pred = yh_pred.collect_data()

    train = MLProphet(data_yh_train, FEATURES, LABEL)
    train.model_fit()

    forecast = train.model_predict(data_yh_pred, window=WINDOW)
    forecast['ds'] = forecast['ds'].astype(str)
    forecast = forecast.to_dict()
    return forecast

# class Stock(Resource):
#     def get(self):
#         TICKER = os.environ.get("TICKER", "msft")
#         # CURRENT_DATE = os.environ.get("CURRENT_DATE", datetime.today().strftime("%Y-%m-%d"))
#         CURRENT_DATE = "2022-01-03"
#         WINDOW = os.environ.get("WINDOW", 1)
#         forecast = train_pred(CURRENT_DATE, TICKER, WINDOW, FEATURES, LABEL)
#         return {'data': forecast}, 200

#     def post(self):
#         parser = reqparse.RequestParser()  # initialize
#         parser.add_argument('ticker', required=True)  # add args
#         parser.add_argument('date', required=True)
#         parser.add_argument('window', required=True)
#         args = parser.parse_args()  # parse arguments to dictionary
#         TICKER = args['ticker']
#         CURRENT_DATE = args['date']
#         WINDOW = int(args['window'])
#         forecast = train_pred(CURRENT_DATE, TICKER, WINDOW, FEATURES, LABEL)
#         return {'data': forecast}, 200


# api.add_resource(Stock, '/Stock')

@app.route('/stockprice/<ticker>', methods=['GET'])
def stockprice(ticker):
    CURRENT_DATE = os.environ.get("CURRENT_DATE", datetime.today().strftime("%Y-%m-%d"))
    start = (datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date() - dt.timedelta(7)).strftime("%Y-%m-%d")
    end = CURRENT_DATE
    yh = yahoo(ticker, start, end)
    data_yh = yh.collect_data()
    data_yh = data_yh.reset_index()
    data_yh = data_yh.to_dict()
    return {'data': data_yh}, 200


@app.route('/stockprediction/<ticker>', methods=['POST'])
def stockprediction(ticker):
    parser = reqparse.RequestParser()  # initialize
    # parser.add_argument('ticker', required=True)  # add args
    parser.add_argument('date', required=True)
    parser.add_argument('window', required=True)
    args = parser.parse_args()  # parse arguments to dictionary
    TICKER = ticker
    CURRENT_DATE = args['date']
    WINDOW = int(args['window'])
    forecast = train_pred(CURRENT_DATE, TICKER, WINDOW, FEATURES, LABEL)
    return {'data': forecast}, 200

if __name__ == '__main__':
    app.run()