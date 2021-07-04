import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List

from secrets import consumer_key, consumer_secret, access_token, access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


class TweetProvider:
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


class Preference:
    def get_preference_score(all_tweets: List[str]) -> List[float]:
        preference_scores = []
        for tweet in all_tweets:
            blob = TextBlob(tweet)
            preference_scores.append(blob.preference.polarity)

        return preference_scores

    def get_avg_preference_score(self, keyword: str) -> int:
        tp = TweetProvider
        tweets = tp.get_tweets(keyword)
        tweets_clean = tp.clean_tweets(tweets)
        preference_scores = self.get_preference_score(tweets_clean)

        average_score = statistics.mean(preference_scores)
        print(average_score)
        return average_score


if __name__ == "__main__":

    pref = Preference
    print("Co lepiej zrobić?")
    first_thing = input()
    print('...czy...')
    second_thing = input()
    print("\n")

    first_score = pref.get_avg_preference_score(first_thing)
    second_score = pref.get_avg_preference_score(second_thing)

    if first_score == second_score:
        print("bez znaczenia")
    elif first_score > second_score:
        print(f"Lepiej jak zrobisz {first_thing} zamiast {second_thing}")
    else:
        print(f"Lepiej jak zrobisz {second_thing} zamiast {first_thing}")
