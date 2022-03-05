from argparse import ArgumentParser
from model import MLProphet
from data_extract import extract, yahoo
from sklearn.metrics import r2_score

feature = ['High','Low','Close','Adj Close','Volume']
label = ['Open']

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--ticker', help='the ticker of stock', type=str)
    # parser.add_argument('--feature', help='the input feature',  type=str)
    # parser.add_argument('--label', help='the target predicted variable',  type=str)
    parser.add_argument('--train_start', help='the start of training date', type=str)
    parser.add_argument('--train_end', help='the end of raining date', type=str)
    parser.add_argument('--pred_start', help='the start of prediction date', type=str)
    parser.add_argument('--pred_end', help='the end of prediction date', type=str)
    args = parser.parse_args()
    # print(args.feature)
    # print(args.label)
    print(args.ticker)
    print(args.train_start)
    yh_train = yahoo(args.ticker, args.train_start, args.train_end)
    data_yh_train = yh_train.collect_data()
    train = MLProphet(data_yh_train, feature, label)
    model = train.model_fit()

    yh_pred = yahoo(args.ticker, args.pred_start, args.pred_end)
    data_yh_pred = yh_pred.collect_data()
    pred = MLProphet(data_yh_pred, feature, label)
    forecast = pred.model_predict(model)
    print(r2_score(forecast.y_true, forecast.yhat))
