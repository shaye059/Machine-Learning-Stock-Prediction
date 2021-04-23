import sys
import pandas as pd
import yfinance as yf
from datetime import date, timedelta


def get_stock_time(published):
    published_date = published[0:10]
    published_date = date(int(published_date[0:4]), int(published_date[5:7]), int(published_date[8:10]))

    # Check if the article was published on a trading day
    is_market_day = bool(len(pd.bdate_range(published_date, published_date)))

    # If it was a market day, see if it was published during trading hours
    if is_market_day:
        time = published[11:-1]

        # If the article was published before trading hours, compare the price from
        # the close of the previous day to the open of the current day.
        if time < '09:30:00':
            prev_day = published_date - timedelta(1)
            prev_market_day = bool(len(pd.bdate_range(prev_day, prev_day)))
            while not prev_market_day:
                prev_day = prev_day - timedelta(1)
                prev_market_day = bool(len(pd.bdate_range(prev_day, prev_day)))

            # A time delta of one day is added to each end day since yFinance only
            # retrieves data upto and NOT including the end date.
            end = published_date + timedelta(1)

            return prev_day, end

        # The market typically closes at 16:00 (4pm) but the later limit
        # will be set to 15:30 (3:30pm) since most people will not have seen it
        # within the 30 minutes before closing. Compare close of current day to open
        # of next market day.
        elif time > '15:30:00':
            next_day = published_date + timedelta(1)
            next_market_day = bool(len(pd.bdate_range(next_day, next_day)))
            while not next_market_day:
                next_day = next_day + timedelta(1)
                next_market_day = bool(len(pd.bdate_range(next_day, next_day)))
            end = next_day + timedelta(1)
            return published_date, end

        # The article was published during market hours so compare opening of
        # current day to close of current day
        else:
            return published_date, published_date + timedelta(1)

    # The article was posted on a day that the market was closed so compare the
    # close of the last market day to the opening of the next.
    else:
        prev_day = published_date - timedelta(1)
        prev_market_day = bool(len(pd.bdate_range(prev_day, prev_day)))
        next_day = published_date + timedelta(1)
        next_market_day = bool(len(pd.bdate_range(next_day, next_day)))
        while not prev_market_day:
            prev_day = prev_day - timedelta(1)
            prev_market_day = bool(len(pd.bdate_range(prev_day, prev_day)))
        while not next_market_day:
            next_day = next_day + timedelta(1)
            next_market_day = bool(len(pd.bdate_range(next_day, next_day)))
        next_day = next_day + timedelta(1)
        return prev_day, next_day


def price_getter(row, ticker_data):
    try:
        ticker = ticker_data[row['ticker']].history(interval='1d', start=str(row['start']), end=str(row['end']))
        if len(ticker) == 1:
            day = ticker.iloc[0]
            delta = (day['Close'] - day['Open']) / day['Open'] * 100
            return delta

        if len(ticker) == 2:
            day1 = ticker.iloc[0]
            day2 = ticker.iloc[1]
            delta = (day2['Open'] - day1['Close']) / day1['Close'] * 100
            return delta

    except:
        print('Error retrieving values from yFinance, try running first cell again')


if __name__ == '__main__':
    try:
        articles = pd.read_csv('../News_Articles.csv')

    except FileNotFoundError:
        print("ERROR: Couldn't find 'News_Articles.csv'.")
        sys.exit()

    articles['publishedAt'] = articles['publishedAt'].astype(str)

    articles['start'], articles['end'] = zip(*articles['publishedAt'].apply(get_stock_time))

    articles['ticker'] = articles['ticker'].astype(str)

    tickers = articles.ticker.unique()


    tickerData = {}
    for ticker in tickers:
        tickerData[ticker] = yf.Ticker(ticker)

    # TODO: Only feed the articles that don't have stock prices yet into this, otherwise it's slow
    articles['delta'] = articles.apply(price_getter, ticker_data=tickerData, axis=1)

    articles.to_csv('tester.csv')

