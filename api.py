from flask import Flask
from flask_restful import Resource, Api, reqparse
from src.SigmaModel import SigmaModel
from src.data_extract import yahoo
from sklearn.metrics import r2_score
from datetime import datetime
import datetime as dt
import os


app = Flask(__name__)
api = Api(app)


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
    model = SigmaModel(TICKER, CURRENT_DATE)
    predictions = model.predict(WINDOW)
    return {'data': predictions}, 200

if __name__ == '__main__':
    app.run()