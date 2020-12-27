"""
This is a Twitter scraper that performs the following tasks:
> connects to Twitter's Streaming API
> filters tweets by keywords
> removes spam
> stores tweet
"""

import os
import string
import time
from enum import Enum

import tweepy
from nameko.standalone.rpc import ClusterRpcProxy

# environment variable names
ENV_AMQP_URI = "AMQP_URI"
ENV_CONSUMER_KEY = "TWITTER_API_CONSUMER_KEY"
ENV_CONSUMER_SECRET = "TWITTER_API_CONSUMER_SECRET"
ENV_ACCESS_TOKEN = "TWITTER_API_ACCESS_TOKEN"
ENV_ACCESS_TOKEN_SECRET = "TWITTER_API_ACCESS_TOKEN_SECRET"
ENV_FILTER = "TWITTER_API_FILTER"

# raise error if variable is not set
if f"{ENV_AMQP_URI}" not in os.environ:
    raise KeyError(f"{ENV_AMQP_URI} is undefined")
if f"{ENV_CONSUMER_KEY}" not in os.environ:
    raise KeyError(f"{ENV_CONSUMER_KEY} is undefined")
if f"{ENV_CONSUMER_SECRET}" not in os.environ:
    raise KeyError(f"{ENV_CONSUMER_SECRET} is undefined")
if f"{ENV_ACCESS_TOKEN}" not in os.environ:
    raise KeyError(f"{ENV_ACCESS_TOKEN} is undefined")
if f"{ENV_ACCESS_TOKEN_SECRET}" not in os.environ:
    raise KeyError(f"{ENV_ACCESS_TOKEN_SECRET} is undefined")
if f"{ENV_FILTER}" not in os.environ:
    raise KeyError(f"{ENV_FILTER} (search term) is undefined")


class Twitter(Enum):
    """
    Twitter API keys enum
    """
    CONSUMER_KEY = os.environ.get(f"{ENV_CONSUMER_KEY}")
    CONSUMER_SECRET = os.environ.get(f"{ENV_CONSUMER_SECRET}")
    ACCESS_TOKEN = os.environ.get(f"{ENV_ACCESS_TOKEN}")
    ACCESS_TOKEN_SECRET = os.environ.get(f"{ENV_ACCESS_TOKEN_SECRET}")
    FILTER = os.environ.get(f"{ENV_FILTER}")


class TweetFilter(object):
    """
    Accepts a tweet Object and provides a set of filtering methods
    """

    banned_terms = ['bitcoin gold', 'bitcoin cash']

    def __init__(self, tweet):
        self.tweet = self.filterTweetData(tweet)
        self.valid_tweet = True

    def should_accept(self):
        return self.is_valid_client().is_pure().get_valid_status()

    def is_valid_client(self):
        if (
            not (
                self.tweet["source"].startswith('Twitter')
                or self.tweet["source"].startswith('TweetDeck')
                or self.tweet["source"].startswith("Tweetbot")
            )
            or (self.tweet["source"].startswith('Twitter Ads'))
        ):
            self.valid_tweet = False
        return self

    def is_not_retweet(self):
        if self.tweet["text"].lower().startswith("rt"):
            self.valid_tweet = False
        return self

    def is_pure(self):
        if any(x in self.tweet["text"].lower() for x in self.banned_terms):
            self.valid_tweet = False
        return self

    def get_valid_status(self):
        return self.valid_tweet

    def filterTweetData(self, tweet):
        # Filters tweet json data to only keep what's required for analysis
        text = tweet.text
        if tweet.truncated:
            text = tweet.extended_tweet["full_text"]

        rt = {
            "id": tweet.id,
            "created_at": tweet._json["created_at"],
            "text": text,
            "source": tweet.source,  # TODO remove this after analyzing sources
            "coordinates": tweet.coordinates,
            "user_id": tweet.user.id,
            "user_is_verified": tweet.user.verified,
            "user_followers_count": tweet.user.followers_count,
            "user_listed_count": tweet.user.listed_count
        }

        self.tweet = rt
        return rt


class MyStreamListener(tweepy.StreamListener):
    """
    Override tweepy.StreamListener to add logic to on_status
    """

    def on_status(self, status):
        tweet_filter = TweetFilter(status)
        if tweet_filter.should_accept():
            callRpc(tweet_filter.tweet)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print("Error 420")
            time.sleep(30)
            return False


def callRpc(tweet):
    """
    Post tweet to the microservice for processing
    """
    with ClusterRpcProxy({"AMQP_URI": os.environ.get(f"{ENV_AMQP_URI}")}) as rpc:
        rpc.scraper_microservice.on_tweet(tweet)


def authenticate():
    """
    Initialise tweepy and auth with Twitter
    """
    auth = tweepy.OAuthHandler(Twitter.CONSUMER_KEY.value,
                               Twitter.CONSUMER_SECRET.value)
    auth.set_access_token(Twitter.ACCESS_TOKEN.value,
                          Twitter.ACCESS_TOKEN_SECRET.value)
    api = tweepy.API(auth)
    return auth, api


if __name__ == "__main__":
    """
    Start Twitter stream listener
    """
    print(f"Starting the Twitter scraper with filter: {Twitter.FILTER.value}")
    auth, api = authenticate()
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(languages=["en"], track=[f"{Twitter.FILTER.value}"])
