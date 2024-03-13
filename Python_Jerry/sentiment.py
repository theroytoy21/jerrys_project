from nltk.tokenize import TweetTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import re
from textblob import TextBlob
from tweet_lookup import main
import datetime
import csv

#roychun21@gmail.com
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('omw-1.4')
stop_words = nltk.corpus.stopwords.words(['english'])

lem = WordNetLemmatizer()

def cleaning(tweet):
    no_url = re.sub(r'http\S+', ' ', tweet)
    no_ht = re.sub(r'#\w+', ' ', no_url)
    no_mention = re.sub(r'@\w+', ' ', no_ht)
    no_mention = re.sub(r'&amp+', ' ', no_ht)
    pre_clean = re.sub('[^A-Za-z]+', ' ', no_mention)

    tweet_tokens = TweetTokenizer().tokenize(pre_clean)
    no_punc = [a for a in tweet_tokens if a.isalnum()]
    no_stop = [a for a in no_punc if a not in stop_words]

    clean = [lem.lemmatize(a) for a in no_stop]
    return ' '.join(clean)

def fetch_tweets(ticker, result_num):
    tweets = main(ticker, result_num)
    cleaned_tweets = []
    for tweet in tweets:
        cleaned_tweets.append(cleaning(tweet))
    return cleaned_tweets

def sentiment(query, result_num):
    tweets = fetch_tweets(query, result_num)
    pos = 0
    neg = 0
    neutral = 0
    scores = []
    date = (datetime.datetime.utcnow()).strftime("%Y-%m-%d")

    for tweet in tweets:
        polarity = TextBlob(tweet).sentiment.polarity
        scores.append(polarity)
        if polarity > 0:
            pos += 1
        elif polarity == 0:
            neutral += 1
        else:
            neg += 1
    sentiment_score = average(scores)
    return {'positive':pos, 'negative':neg, 'neutral':neutral,'avg': sentiment_score, 'date': date}

def average(lst):
  if lst:
    return sum(lst) / len(lst)
  return 'Not tweets'

# tweets can fetch from 10 to 100 tweets only as of 9/29/2023
# dates are returned as UTC time zone

with open("esg_history.csv", 'r') as csvfile:
    file = csv.reader(csvfile)
    i = 0
    big_list = []
    for line in file:
        if i != 0:
            big_list.append(line)
        i = 69

with open("sentiment_scores.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name', 'ESG Score', 'Sentiment', 'Date'])
    for list in big_list:
        list[2] = 0.9 # sentiment change
        list.append(datetime.datetime.utcnow().strftime("%Y-%m-%d"))
    writer.writerows(big_list)

with open('sentiment_scores.csv') as input, open('sentiment_scores_noblanklines.csv', 'w', newline='') as output:
     writer = csv.writer(output)
     for row in csv.reader(input):
         if any(field.strip() for field in row):
             writer.writerow(row)

# ['Apple Inc'(use tickers if easier), '80', '0.19', '2023-09-30']
# ESG Score should be retrieved from the esg_history.csv file
# Save all results into a new csv file as depicted in the example list above.

#print(sentiment("AAPL", 10))