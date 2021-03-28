from newsapi.newsapi_client import NewsApiClient
import pandas as pd
import os

news_key = os.environ['NEWS_API_KEY']

newsapi = NewsApiClient(api_key=news_key) #Your Key Here

articles = pd.read_csv('News_Articles.csv')
print('%d rows in dataframe to start.' % articles.shape[0])

list_of_articles = []
dict_of_companies = {'Microsoft': 'MSFT','Apple':'AAPL','Amazon':'AMZN',
                     'Alphabet':'GOOGL','Facebook':'FB','Intel':'INTC',
                     'Cisco Systems':'CSCO','Comcast':'CMCSA','Adobe':'ADBE',
                     'Nvidia':'NVDA','Netflix':'NFLX','PayPal':'PYPL',
                     'Broadcom':'AVGO','Alibaba':'BABA','AT&T':'T',
                     'Tencent':'TCEHY','Taiwan Semiconductor':'TSM',
                     'Verizon':'VZ', 'Oracle':'ORCL','Tesla':'TSLA',
                     'Qualcomm':'QCOM','Texas Instruments':'TXN','Fiserv':'FISV',
                     'Booking Holdings':'BKNG','Intuit':'INTU','ADP':'ADP',
                     'T-Mobile':'TMUS','Micron':'MU','SAP':'SAP',
                     'Salesforce':'CRM','IBM':'IBM','VMware':'VMW',
                     'Samsung':'005930.KS','Foxconn':'2354.TW','Dell':'DELL',
                     'Sony':'SNE','Panasonic':'PCRFY','HP':'HP',
                     'Berkshire Hathaway':'BRK-A','Visa':'V','Walmart':'WMT',
                     'Johnson & Johnson':'JNJ','Procter & Gamble':'PG',
                     'Mastercard':'MA','JPMorgan Chase':'JPM','UnitedHealth':'UNH',
                     'Home Depot':'HD','Disney':'DIS','Bank of America':'BA',
                     'Coca-Cola':'KO','	Pfizer':'PFE','Novartis AG':'NVS',
                     'Toyota':'TM','Abbott Laboratories':'ABT','Nike':'NKE',
                     'ExxonMobil':'XOM','AbbVie':'ABBV',
                     'Thermo Fisher Scientific':'TMO','McDonalds':'MCD',
                     'ASML':'ASML','Costco Wholesale':'COST','Chevron':'CVX',
                     'Accenture':'ACN','Amgen':'AMGN','Eli Lilly':'LLY',
                     'Medtronic':'MDT'}


for company,ticker in dict_of_companies.items():
    temp = newsapi.get_everything(
                                        language='en',
                                        q=company)['articles']
    for article in temp[:1]:
        article['company'] = company
        article['ticker'] = ticker
        article['source'] = str(article['source'])
        list_of_articles.append(article)


scraped = pd.DataFrame(list_of_articles)
print('Adding %d unseen articles to dataset.' % scraped.shape[0])
articles = articles.append(scraped)
articles = articles.drop_duplicates(ignore_index=True)
articles.to_csv('News_Articles.csv', encoding='utf-8', index=False)