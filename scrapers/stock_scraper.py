import math
import sys
import pandas as pd
from datetime import date, timedelta

try:
    articles = pd.read_csv('../News_Articles.csv')

except FileNotFoundError:
    print("ERROR: Couldn't find 'News_Articles.csv'.")
    sys.exit()


temp_list = articles.to_dict('records')
temp_list2 = list(filter(lambda i: type(i['publishedAt']) != float, temp_list))
article_data = list(filter(lambda i: type(i['ticker']) != float, temp_list2))

for article in article_data:
    if not (type(article['publishedAt']) == float):
        published = article['publishedAt']
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

                article['start'], article['end'] = (prev_day, end)

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
                article['start'], article['end'] = published_date, end

            # The article was published during market hours so compare opening of
            # current day to close of current day
            else:
                article['start'] = published_date
                article['end'] = published_date + timedelta(1)

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
        article['start'] = prev_day
        article['end'] = next_day + timedelta(1)