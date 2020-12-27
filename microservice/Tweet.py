"""
This module includes the Tweet class and related data structures
"""


class Tweet(object):
    coordinates = ""
    created_at = ""
    source = ""
    text = ""
    text_normal = ""
    tweet_id = 0
    user_followers_count = 0
    user_id = 0
    user_is_verified = False
    user_listed_count = 0

    def __init__(self, raw_tweet):
        if raw_tweet is not None:
            self.coordinates = raw_tweet['coordinates']
            self.created_at = raw_tweet['created_at']
            self.source = raw_tweet['source']
            self.text = raw_tweet['text']
            self.tweet_id = raw_tweet['id']
            self.user_followers_count = raw_tweet['user_followers_count']
            self.user_id = raw_tweet['user_id']
            self.user_is_verified = raw_tweet['user_is_verified']
            self.user_listed_count = raw_tweet['user_listed_count']

    def toCleanDict(self):
        return {
            "tweet_id": self.tweet_id,
            "created_at": self.created_at,
            "text": TweetNormalizer(self.text).normalize(),
            "source": self.source,
            "coordinates": self.coordinates,
            "user_id": self.user_id,
            "user_is_verified": self.user_is_verified,
            "user_followers_count": self.user_followers_count,
            "user_listed_count": self.user_listed_count
        }


class TweetNormalizer(object):
    """
    Accepts a text string and provides a set of normalizing methods
    """

    def __init__(self, tweet):
        self.tweet = tweet

    def normalize(self):
        return self.lowercase().strip_whitespace().get_text()

    def lowercase(self):
        self.tweet = self.tweet.lower()
        return self

    def strip_whitespace(self):
        self.tweet = ' '.join(self.tweet.split())
        return self

    def get_text(self):
        return self.tweet
