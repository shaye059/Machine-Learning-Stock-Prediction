# Machine-Learning-Stock-Prediction
The goal of this project is to use Natural Language Processing and Machine Learning to predict the effects of news stories on company stock prices.

The most up to date dataset is available from here: [Processed_Articles.csv](https://drive.google.com/file/d/16QEyw-RJN8C_0mR0M_MBJgX9fuZkOSc5/view?usp=sharing)

To run the scraping you'll need the following libraries:
```
pip install pandas newsapi-python yfinance
```
You'll also need to sign up for an [API key](https://newsapi.org/s/google-news-api) and set it as an environment 
variable named NEWS_API_KEY.

To view the current notebook you can open it in Colab [here](https://colab.research.google.com/github/shaye059/Machine-Learning-Stock-Prediction/blob/master/Stock_Prediction.ipynb)
. This started out as just a small little Notebook experiment but seeing as the developer edition of the news API is
limited to pulling the last 30 days I realized that to build a usable dataset I'd have to set up routine scrapers. The
notebook itself is currently being broken down into modularized scripts and therefore is probably not runnable if you
want to use the already scraped and processed data provided in the CSV. 
