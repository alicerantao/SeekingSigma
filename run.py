import os
from datetime import datetime

from src.SigmaModel import SigmaModel

TICKER = os.environ.get("TICKER", "tsla")
# TODO: Adjust dates and window based on weekday and weekends.
CURRENT_DATE = os.environ.get("CURRENT_DATE", datetime.today().strftime("%Y-%m-%d"))
# CURRENT_DATE = "2022-04-05"
WINDOW = os.environ.get("WINDOW", 3)


if __name__ == "__main__":

    model = SigmaModel(TICKER, CURRENT_DATE)
    predictions = model.predict(WINDOW)

    print(predictions)
