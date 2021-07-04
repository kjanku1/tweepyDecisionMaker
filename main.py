import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List

# from secrets import consumer_key, consumer_secret

consumer_key = "JlugTyoPRwHCAo9RL8oW4rvef"
consumer_secret = "SV1DkRNC9fT1WqBHyoZfH9GuveGk6t8n7W5MRUyxaAFjjBOJqQ"
access_token = "1411541778268934144-0vTefLgDqo52tXvJUj2EyOqSYVxIBG"
access_secret = "APp55i1EicgjwCYKl1yrjnE3EKP5Vk0BW0BOQuG0p6kK6"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode='extended', lang='pl').items(10):
        all_tweets.append(tweet.full_text)

    return all_tweets


def clean_tweets(all_tweets: List[str]) -> List[str]:
    tweets_clean = []
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))

    return tweets_clean


def get_sentiment(all_tweets: List[str]) -> List[float]:
    sentiment_scores = []
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)

    return sentiment_scores


def get_avg_sentiment_score(keyword: str) -> int:
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)

    average_score = statistics.mean(sentiment_scores)
    print(average_score)
    return average_score


if __name__ == "__main__":
    print("Co lepiej zrobić?")
    first_thing = input()
    print('...czy...')
    second_thing = input()
    print("\n")

    first_score = get_avg_sentiment_score(first_thing)
    second_score = get_avg_sentiment_score(second_thing)

    if (first_score > second_score):
        print(f"Lepiej jak zrobisz {first_thing} zamiast {second_thing}")
    else:
        print(f"Lepiej jak zrobisz {second_thing} zamiast {first_thing}")