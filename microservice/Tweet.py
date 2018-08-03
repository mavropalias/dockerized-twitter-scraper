"""
This module includes the Tweet class and related data structures
"""


class Tweet(object):
    tweet_id = 0
    created_at = ""
    text = ""
    text_normal = ""
    source = ""
    coordinates = ""

    user_id = 0
    user_is_verified = False
    user_followers_count = 0
    user_listed_count = 0

    def __init__(self):
        pass

    def cleanup_and_analyze(self):
        self.normalize()

    def normalize(self):
        self.text_normal = TweetNormalizer(self.text).normalize()


class TweetNormalizer(object):
    """
    Accepts a text string and provides a set of normalizing methods
    """

    def __init__(self, tweet):
        self.tweet = tweet

    def normalize(self):
        # TODO remove retweets
        return self.lowercase().strip_whitespace().get_text()

    def lowercase(self):
        self.tweet = self.tweet.lower()
        return self

    def strip_whitespace(self):
        self.tweet = ' '.join(self.tweet.split())
        return self

    def get_text(self):
        return self.tweet
