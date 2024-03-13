import requests
import pandas as pd
from textblob import TextBlob
import csv
import datetime
from esg_info import esg_getter

def main(company):
    payload = {
        'api_key': '18cb9d9ab815073c60c9138449e8840a',
        'query': company,
        'num': '10',
        'time_period': '1D'
    }

    response = requests.get('https://api.scraperapi.com/structured/twitter/search', params=payload)
    data = response.json()

    print(data)
    all_tweets = data['organic_results']
    # print(all_tweets)

    twitter_data = []
    for tweet in all_tweets:
        print(tweet["snippet"].split("— "))
        twitter_data.append(tweet["snippet"].split("— ")[1])
        
    # sentiment_list = []
    # for text in twitter_data:
    #     sentiment_list.append(get_sentiment(preprocess_text(str(text))))
    sentiment_list = get_sentiment(preprocess_text(twitter_data))
    print(sentiment_list)

    with open("training_data.csv", 'a', newline="") as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(["Tweet Count","Sentiment","Positive","Negative","Neutral","Date(UTC)","Company Name","ESG"])
        writer.writerow([
                        str(len(twitter_data)),
                        str(max_sentiment(sentiment_list)),
                        str(sentiment_list[0]),
                        str(sentiment_list[1]),
                        str(sentiment_list[2]),
                        str(date),
                        str(payload['query']),
                        str(esg_getter(payload['query']))
                        ])

def preprocess_text(list):
    for tweet in list:
        str(tweet.lower().split())
    return list

def get_sentiment(list):
    positive = 0
    negative = 0
    neutral = 0
    for tweet in list:
        blob = TextBlob(str(tweet))
        polarity = blob.sentiment.polarity
        if polarity > 0:
            positive += 1
        elif polarity < 0:
            negative += 1
        else:
            neutral += 1
    return [positive, negative, neutral]

def max_sentiment(list):
    if (list[0] >= list[1]) and (list[0] >= list[2]):
        return "positive"
    elif (list[1] >= list[0]) and (list[1] >= list[2]):
        return "negative"
    else:
        return "neutral"


    # df = pd.DataFrame(twitter_data)

    # chart = df.head(int(payload['num']))
    # print(chart)

def real_main():
    companys = ["AAPL","AMZN","MSFT","TSLA","GOOG"]
    for company in companys:
        main(company)

date = str((datetime.datetime.utcnow()).strftime("%Y-%m-%d"))
with open("training_data.csv", 'r') as csvfile:
    file = csv.reader(csvfile)
    latest_date = csvfile.readlines()[-1]
    if latest_date.find(date) == -1:
        real_main()
    else:
        print("Already searched today.")